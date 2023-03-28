"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, Mapping, Any, List, Optional, Callable

from spil import Sid, Getter, Finder
from spil.conf import default_path_config, path_data_suffix  # type: ignore


class GetByFinder(Getter):
    """
    Some Getters first use a Finder to retrieve the Sids,
    then, in a second distinct step, retrieve the data.
    For example, GetFromPaths which stores data in json "sidecar" files.

    This "GetByFinder" is an abstract Getter, implementing shared methods for Getters that use a Finder.

    These Getters can inherit GetByFinder, and:
    - override the constructor and define self.finder
    - or pass it to the constructor (inherited from GetByFinder)
    - and implement get_data()
    """

    def __init__(self, finder: Finder):
        self.finder = finder

    def get(
        self,
        search_sid: str | Sid,
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        See Getter.
        """
        for sid in self.finder.find(search_sid=search_sid, as_sid=True):
            data = self.get_data(sid, attributes=attributes, sid_encode=sid_encode) or {}
            yield data

    def do_get(
        self,
        search_sids: List[Sid],
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        See Getter.
        """
        for sid in self.finder.do_find(search_sids=search_sids, as_sid=True):
            data = self.get_data(sid, attributes=attributes, sid_encode=sid_encode) or {}
            yield data

    def get_data(
        self, sid: str | Sid, attributes: Optional[List[str]] = None, sid_encode: Callable = str
    ) -> Mapping[str, Any]:
        """
        See Getter.
        """
        raise NotImplementedError("To be used, GetByFinder should be inherited, and get_data overriden.")

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Finder: "{self.finder}"]'


if __name__ == "__main__":
    from spil import FindInPaths

    finder = FindInPaths()
    print(GetByFinder(finder))
