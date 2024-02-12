"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Iterator, List, Set, Optional

import os
import glob

from spil import Sid
from spil import conf
from spil.sid.pathops.pathconfig import get_path_config
from spil.sid.read.finders.find_glob import FindByGlob
from spil.util.exception import SpilException
from spil.util.log import warn, debug, error

try:
    import fileseq  # type: ignore
except ImportError:
    fileseq = None
    warn("fileseq could not be imported. File sequence search will not work.")


class FindInPaths(FindByGlob):
    """

    Searches for sids in a File System.
    Mainly uses the glob search.

    Still Beta.

    """

    def __init__(self, config: Optional[str] = None):
        """
        Config is the desired config_name name, as configured in data_conf.
        If config_name is None, the default config_name (during class instantiation) is used.


        """
        self.config_name = config or conf.default_path_config  # type: ignore
        self.conf = get_path_config(self.config_name)

    def star_search(
        self, search_sids: List[Sid], as_sid: bool = False, do_sort: bool = False
    ) -> Iterator[Sid] | Iterator[str]:
        """
        Star search main function.

        Delegates to "star_search_simple" by default,
        or to "star_search_framed" to handle file sequences, if "frame=*" is in the search

        Args:
            search_sids: list of Sids to search
            as_sid: return the result as sid object or string (the default)
            do_sort: not implemented in FindInPaths (#FIXME correct design)

        Returns:

        """
        if do_sort:
            debug("do_sort not implemented in FindInPaths")

        # depending on input, select the right generator
        # FIXME: hardcoded "frame"
        is_framed_search = any([ssid.get("frame") == "*" for ssid in search_sids])

        if is_framed_search and fileseq:
            generator = self.star_search_framed(search_sids, as_sid=as_sid)
        else:
            generator = self.star_search_simple(search_sids, as_sid=as_sid)

        yield from generator

    def star_search_simple(
        self, search_sids: List[Sid], as_sid: bool = False
    ) -> Iterator[Sid] | Iterator[str]:
        """
        Star search without file sequence handline.

        Uses Glob.

        :param search_sids:
        :param as_sid:
        :return:
        """
        debug("Starting star_search_simple")

        # doublon detection
        searched: dict[str, list] = defaultdict(list)  # already searched patterns by sid type
        found_paths = set()

        for search_sid in search_sids:

            debug('Starting search:  "{}"'.format(repr(search_sid)))

            search = search_sid  # TODO: handle also strings ?

            debug("Search : {}".format(search))
            pattern = str(search.path(self.config_name))

            if not pattern:
                warn("Search sid {} did not resolve to a path. Cancelled.".format(search))
                continue

            for key, value in self.conf.search_path_mapping.items():
                pattern = pattern.replace(key, value)

            debug(f"Search pattern: {pattern}")
            if pattern in searched.get(search.type, []):
                continue
            else:
                searched[search.type].append(pattern)

            debug(f"Now searching pattern: {pattern}")
            found = glob.glob(pattern)
            debug("found")
            debug(found)
            for path in found:
                path = path.replace(os.sep, "/")
                if path in found_paths:
                    continue
                try:
                    sid = Sid(path=path, config=self.config_name)
                    debug(f"found {sid}")
                    if sid.type != search.type:
                        warn(
                            f"Found Sid and search have different types. "
                            f'Consider narrowing the pattern, or implementing "typed_search_narrowing".'
                            f"Found: {sid.uri} -- Search: {search.uri}"
                        )
                        continue
                except SpilException as e:
                    debug(f"Path did not generate sid: {path}")
                    continue
                if not sid:
                    debug(f"Path did not generate sid: {path}")
                    continue

                found_paths.add(path)
                if as_sid:
                    yield sid
                else:
                    yield str(sid)

    def star_search_framed(
        self, search_sids: List[Sid], as_sid: bool = False
    ) -> Iterator[Sid] | Iterator[str]:
        """
        Star search with file sequence handling.

        Uses Glob and fileseq.

        :param search_sids:
        :param as_sid:
        :return:
        """
        debug("Starting star_search_framed")

        searched: Set[str] = set()
        done: Set[str] = set()
        done_add = done.add

        for search_sid in search_sids:

            debug('[fs_star_search] "{}"'.format(search_sid))

            search = search_sid  # TODO: handle also strings ?

            if search.get("frame") == "*":  # FIXME: hardcoded "frame"
                search = search.get_with("frame", "@")  # for usage in fileseq

            debug("Search : " + str(search))
            pattern = str(search.path(self.config_name))

            if not pattern:
                warn("Search sid {} did not resolve to a path. Cancelled.".format(search))
                return

            if pattern in searched:
                continue
            else:
                searched.add(pattern)

            for key, value in conf.search_path_mapping.items():  # type: ignore
                pattern = pattern.replace(key, value)

            dir_pattern, file_pattern = os.path.split(pattern)
            debug(dir_pattern)
            parents = glob.glob(dir_pattern)
            file_sequences = []
            for parent in parents:
                file_search = os.path.join(parent, file_pattern).replace(os.sep, "/")
                debug("search " + file_search)
                file_sequences.extend(fileseq.findSequencesOnDisk(file_search))

            debug("found sequences : {}".format(file_sequences))
            for file_sequence in file_sequences:
                debug(file_sequence)
                path = str(file_sequence[0]).replace(
                    os.sep, "/"
                )  # we get the first file of the sequence
                try:
                    sid = Sid(path=path, config=self.config_name)
                    debug("found " + str(sid))
                except SpilException as e:
                    debug("Path did not generate sid : {}".format(path))
                    continue
                if not sid:
                    warn("Path did not generate sid : {}".format(path))
                    continue

                item = str(sid)
                if item not in done:
                    done_add(item)
                    if as_sid:
                        yield sid
                    else:
                        yield item
                else:
                    debug("{} was already found, skipped. ".format(item))

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config_name}"]'


if __name__ == "__main__":
    print(FindInPaths())
