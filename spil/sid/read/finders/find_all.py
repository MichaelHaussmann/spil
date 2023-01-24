# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterable, List, Dict, Optional

from spil import Sid
from spil.sid.read.finder import Finder

from spil.util.log import debug, info, warning, error
from spil.conf import get_finder_for  # type: ignore
from spil.util.caching import lru_cache as cache
from spil.sid.read.tools import unfold_search


@cache
def get_finder(sid: Sid | str, config: Optional[str] = None) -> Finder | None:
    """
    Calls spil.conf.get_finder_for() which is implemented in the spil_data_conf.

    Retrieves, for a given Search Sid and configuration name, the appropriate Finder and returns it.

    This typically returns a Finder depending on the Type of the Sid.
    For example: projects come from a FindInConstant, Assets and Shots may come from FindInPaths or FindInShotgrid.
    See the example spil_data_conf.get_finder_for()

    Technical note: the result is cached.
    This means that the choice of the Finder is cached, not the resulting data itself.
    The Finder is called again each time a query method (find(), find_one(), exists()) is called.

    Args:
        sid: the Search Sid for which we want to get the appropriate Finder instance
        config: an optional configuration name, to be able to have mutliple configs co-existing.

    Returns:
        the Finder to use for this Search Sid

    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        warning(f'Sid could not be instanced, likely a configuration error. "{sid}" -> {_sid}')
    source = get_finder_for(_sid, config)
    if source:
        debug(f'Getting data source for "{sid}": -> {source}')
        return source
    else:
        warning(f'Data Source not found for Sid "{sid}" ({_sid.type})')
        return None


class FindInAll(Finder):
    """
    This Finder will call other Finders, as configured, depending on the search sids type.

    """
    def __init__(self, config: Optional[str] = None):
        """
        Config is an argument that will be passed to the config, via get_finder_for(sid, config).
        Config acts like a key, to allow multiple FindInAll configurations to co-exist.

        Args:
            config: name of a configuration
        """

        self.config = config

    def find(self, search_sid: str | Sid, as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        """
        Search dispatcher.

        The search is "unfolded" (one possibly untyped search sid is "unfolded" into a list of typed search sids).
        For each typed sid, we get the appropriate Finder.

        We then group the searches by Finder, to call each Finder with a list of searches (instead of each search individually).

        Args:
            search_sid: Sid to search
            as_sid: result will be returned as a Sid object if True, as a string otherwise.

        Returns:
            Generator over the found Sids, as Sid or string instances.
        """
        # we start by transforming
        search_sids = unfold_search(search_sid)

        done = set()  #TEST
        finder_for_searches: Dict[Finder, List[Sid]] = dict()

        for search_sid in search_sids:

            finder = get_finder(search_sid, self.config)  # TODO: allow multiple finders for the same search (eg.

            if finder:
                l = finder_for_searches.get(finder) or list()
                l.append(search_sid)
                finder_for_searches[finder] = l

        for finder, searches in finder_for_searches.items():

            debug(f'Searching "{finder}" --> "{searches}"')
            generator = finder.do_find(searches, as_sid=False)

            for i in generator:
                if i not in done:  # FIXME: check why data is so often repeated, this is expensive, optimize
                    done.add(i)
                    if as_sid:
                        yield Sid(i)
                    else:
                        yield i

            else:
                debug(f'Nothing found for "{search_sid.full_string}"')

    def do_find(self, search_sids: List[Sid], as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        raise NotImplementedError("Find by Type delegates do_find to other Finders, depending on the search type.")

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":
    print(FindInAll())
