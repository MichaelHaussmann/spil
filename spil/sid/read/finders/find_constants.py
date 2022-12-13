# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from __future__ import annotations
from typing import Iterable, List

from spil import Sid, Finder
from spil.sid.read.finders.find_glob import FindByGlob
from spil.util.exception import SpilException
from spil.util.log import debug


class FindInConstants(FindByGlob):
    """
    Finds Sid from a list, for a specific type.

    Whereas FindInList looks inside a list of Sids, FindInConstants looks inside a list for one specific keytype.

    Example:
        ```
        >>> fp = FindInPaths()
        >>> at_fc = FindInConstants('assettype', ['char', 'location', 'prop', 'fx'], parent_source=fp)
        >>> list( at_fc.find('hamlet/a/*') )
        [Sid('hamlet/a/char'), Sid('hamlet/a/location'), Sid('hamlet/a/prop'), Sid('hamlet/a/fx')]
        ```

    Implements star_search for a specific key, by getting the values from a given, constant, list.
    If there is a search "above" the given key, the search is delegated to the given "parent_source".

    This is used to create a Data Source for constant values.

    Still alpha.
    """

    def __init__(self, key: str, values: List[str], parent_source: Finder | None = None):
        self.key = key
        self.values = values
        self.parent_source = parent_source

    def _append_value(self, root: Sid, done: set, as_sid: bool = False) -> Iterable[Sid] | Iterable[str]:

        for value in self.values:

            result = root.get_with(key=self.key, value=value)
            if not result:
                debug(
                    'Generated Sid "{}" is not valid, skipped (built {} with {}:{})'.format(
                        result, result, self.key, value
                    )
                )
                continue

            if result not in done:
                #done.add(result)
                if as_sid:
                    yield result
                else:
                    yield str(result)

    def star_search(self, search_sids: List[Sid],
                    as_sid: bool = False,
                    do_sort: bool = False) -> Iterable[Sid] | Iterable[str]:

        done = set()

        for search_sid in search_sids:

            root = Sid(search_sid).get_as(self.key)

            if not root:
                continue

            if "*" not in str(root):

                if root not in done:
                    #done.add(root)  # FIXME: check why data is so often repeated, this is expensice, optimize
                    if as_sid:
                        yield root
                    else:
                        yield str(root)

            elif "*" in str(root.parent) and root != root.parent:

                if not self.parent_source:
                    raise SpilException(
                        "The parent of {} is itself a search, but no parent_source was given.".format(
                            root
                        )
                    )

                for found_root in self.parent_source.get(root):

                    if root.get(self.key) != "*":
                        result = found_root / root.get(self.key)
                        if result not in done:
                            #done.add(result)
                            if as_sid:
                                yield result
                            else:
                                yield str(result)
                    else:
                        generator = self._append_value(found_root, done, as_sid=as_sid)
                        for i in generator:
                            yield i
            else:

                generator = self._append_value(root, done, as_sid=as_sid)
                for i in generator:
                    yield i

    def __str__(self) -> str:
        return f'[FindInConstants] key: "{self.key}" / values: {self.values} / parent source: \n\t"{self.parent_source}"'


if __name__ == "__main__":

    from spil.conf import projects, asset_types
    from spil.util.log import setLevel, WARN

    setLevel(WARN)

    cs1 = FindInConstants("project", projects)
    cs2 = FindInConstants("type", ["a", "s"], parent_source=cs1)
    cs3 = FindInConstants('assettype', asset_types, parent_source=cs2)
    cs4 = FindInConstants('sequence', ['sq088'], parent_source=cs2)
    print(cs2)

    for i in cs1.find("*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print('-' * 20)

    for i in cs2.find("hamlet/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print('-' * 20)

    for i in cs3.find("hamlet/*/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print('-' * 20)

    for i in cs4.find("hamlet/*/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print('-' * 20)

