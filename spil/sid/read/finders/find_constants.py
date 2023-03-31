"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, List

from spil import Sid, Finder
from spil.sid.read.finders.find_glob import FindByGlob
from spil.util.exception import SpilException
from spil.util.log import debug


class FindInConstants(FindByGlob):
    """
    Finds Sid from a list, for a specific type.

    Whereas FindInList looks inside a list of Sids, FindInConstants looks inside a list for one specific keytype.

    Implements star_search for a specific key, by getting the values from a given, constant, list.
    If there is a search "above" the given key, the search is delegated to the given "parent_source".

    This is used to create a Data Source for constant values.

    Examples:

        We instantiate a parent Finder

            >>> from spil import FindInPaths
            >>> fp = FindInPaths()

        Finding a constant list of asset types

            >>> finder = FindInConstants('assettype', ['char', 'location', 'prop', 'fx'], parent_source=fp)
            >>> list( finder.find('hamlet/a/*') )
            [Sid('asset__assettype:hamlet/a/char'), Sid('asset__assettype:hamlet/a/location'), Sid('asset__assettype:hamlet/a/prop'), Sid('asset__assettype:hamlet/a/fx')]

        Search "above" in the hierarchy is delegated to the parent

            >>> list( finder.find('hamlet/*/prop') )
            [Sid('asset__assettype:hamlet/a/prop')]

        Other examples, defining a constant list of "states" and searching for states

            >>> finder_states = FindInConstants('state', ["w", "p"], parent_source=fp)
            >>> list( finder_states.find('hamlet/a/location/ramparts/rig/v001/*') )
            [Sid('asset__state:hamlet/a/location/ramparts/rig/v001/w'), Sid('asset__state:hamlet/a/location/ramparts/rig/v001/p')]

        Finding a state with a parent search

            >>> list( finder_states.find('hamlet/a/location/ramparts/rig/*/p') )
            [Sid('asset__state:hamlet/a/location/ramparts/rig/v001/p'), Sid('asset__state:hamlet/a/location/ramparts/rig/v002/p')]

        Finding a state with a multi-parent search

            >>> sorted(list( finder_states.find('hamlet/a/location/*/rig/*/p') ))
            [Sid('asset__state:hamlet/a/location/elsinore/rig/v001/p'), Sid('asset__state:hamlet/a/location/elsinore/rig/v002/p'), Sid('asset__state:hamlet/a/location/garden/rig/v001/p'), Sid('asset__state:hamlet/a/location/garden/rig/v002/p'), Sid('asset__state:hamlet/a/location/lakeside/rig/v001/p'), Sid('asset__state:hamlet/a/location/lakeside/rig/v002/p'), Sid('asset__state:hamlet/a/location/queens_chamber/rig/v001/p'), Sid('asset__state:hamlet/a/location/queens_chamber/rig/v002/p'), Sid('asset__state:hamlet/a/location/ramparts/rig/v001/p'), Sid('asset__state:hamlet/a/location/ramparts/rig/v002/p')]

        Combining parent and constant search

            >>> list( finder_states.find('hamlet/a/location/ramparts/rig/*/*') )
            [Sid('asset__state:hamlet/a/location/ramparts/rig/v001/w'), Sid('asset__state:hamlet/a/location/ramparts/rig/v001/p'), Sid('asset__state:hamlet/a/location/ramparts/rig/v002/w'), Sid('asset__state:hamlet/a/location/ramparts/rig/v002/p')]

        Finds itself if needed.

            >>> list( finder_states.find('hamlet/a/location/ramparts/rig/v001/p') )
            [Sid('asset__state:hamlet/a/location/ramparts/rig/v001/p')]

    This is still beta code.
    """

    def __init__(self, key: str, values: List[str], parent_source: Finder | None = None):  # noqa
        """


        Args:
            key: the keytype for which this Finder operates.
            values: the list of values that this Finder always finds, for the given key.
            parent_source: delegates to this finder for searches above the keytype (parents of the keytype)
        """
        self.key = key
        self.values = values
        self.parent_source = parent_source

    def _append_value(
        self, root: Sid, done: set, as_sid: bool = False
    ) -> Iterator[Sid] | Iterator[str]:
        """
        This method fills the keytype with the values, by appending them to the parent root.

        Args:
            root:
            done:
            as_sid:

        Returns:
        """

        for value in self.values:

            result = root.get_with(key=self.key, value=value)
            if not result:
                debug(f'Generated Sid "{result}" is not valid, skipped (used {self.key}:{value})')
                continue

            if result not in done:
                # done.add(result)
                if as_sid:
                    yield result
                else:
                    yield str(result)

    def star_search(
        self, search_sids: List[Sid], as_sid: bool = False, do_sort: bool = False
    ) -> Iterator[Sid] | Iterator[str]:

        done = set()

        for search_sid in search_sids:

            root = Sid(search_sid).get_as(self.key)

            if not root:
                continue

            # nothing to search, we yield
            if "*" not in str(root):

                if root not in done:
                    # done.add(root)  # TODO: useful ?
                    if as_sid:
                        yield root
                    else:
                        yield str(root)

            # the parent needs to be searched
            elif "*" in str(root.parent) and root != root.parent:

                if not self.parent_source:
                    raise SpilException(
                        f"The parent of {root} is a search, but no parent_source was given."
                    )

                for found_root in self.parent_source.find(root.parent):

                    # the constant "key" is not searched
                    # we can simply yield the parent and the key's value
                    if root.get(self.key) != "*":
                        result = found_root / root.get(self.key)
                        if result not in done:
                            # done.add(result)
                            if as_sid:
                                yield result
                            else:
                                yield str(result)

                    # the "key" is a search, so we append the constant values
                    else:
                        generator = self._append_value(found_root, done, as_sid=as_sid)
                        yield from generator

            # no parent search, we just need to append the constant values
            else:
                generator = self._append_value(root, done, as_sid=as_sid)
                yield from generator

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Key: "{self.key}" -- values: {self.values} -- parent source: \n\t"{self.parent_source}"]'


if __name__ == "__main__":

    from spil.conf import projects, asset_types
    from spil.util.log import setLevel, WARN

    setLevel(WARN)

    cs1 = FindInConstants("project", projects)
    cs2 = FindInConstants("type", ["a", "s"], parent_source=cs1)
    cs3 = FindInConstants("assettype", asset_types, parent_source=cs2)
    cs4 = FindInConstants("sequence", ["sq088"], parent_source=cs2)
    print(cs2)

    for i in cs1.find("*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print("-" * 20)

    for i in cs2.find("hamlet/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print("-" * 20)

    for i in cs3.find("hamlet/*/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print("-" * 20)

    for i in cs4.find("hamlet/*/*"):
        print(f"sid: {i} / {type(i)} / path: {i.path()}")
    print("-" * 20)
