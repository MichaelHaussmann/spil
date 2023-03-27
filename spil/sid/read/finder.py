"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, List, overload, Optional
from typing_extensions import Literal

from spil.sid.sid import Sid
from spil.sid.read.util import first
from spil.sid.read.tools import unfold_search


class Finder:
    """
    Interface for Sid Finder.

    Implements common public Sid Search methods "find", "find_one", and "exists"

    The search process is as follows:
        find():
        - the search sid string is "unfolded" into a list of typed search Sids.

        do_find()
        - runs the actual search on each typed search sid
    """

    @overload
    def find(self, search_sid: str, as_sid: Literal[True]) -> Iterator[Sid]:
        ...

    @overload
    def find(self, search_sid: str, as_sid: Literal[False]) -> Iterator[str]:
        ...

    @overload
    def find(self, search_sid: Sid, as_sid: Literal[True]) -> Iterator[Sid]:
        ...

    @overload
    def find(self, search_sid: Sid, as_sid: Literal[False]) -> Iterator[str]:
        ...

    @overload
    def find(self, search_sid: str) -> Iterator[Sid]:
        ...

    @overload
    def find(self, search_sid: Sid) -> Iterator[Sid]:
        ...

    def find(
        self, search_sid: str | Sid, as_sid: Optional[bool] = True
    ) -> Iterator[Sid] | Iterator[str]:
        """
        Yields the Sids found using the given search_sid.
        Returns a generator over Sids, if as_sid is True (default), or over Sid strings.

        Example:

            >>> from spil import FindInAll
            >>> list(FindInAll().find('hamlet/a/*'))
            [Sid('asset__assettype:hamlet/a/char'), Sid('asset__assettype:hamlet/a/location'), Sid('asset__assettype:hamlet/a/prop'), Sid('asset__assettype:hamlet/a/fx')]

        Args:
            search_sid: typed or untyped Sid or string
            as_sid: if the result should be Sid objects or strings

        Returns:
            Generator over Sids or strings
        """
        # shortcut if Sid is not a search
        sid = Sid(search_sid)
        if sid and not sid.is_search():
            generator = self.do_find([sid], as_sid=as_sid)
        else:
            search_sids = unfold_search(search_sid)
            generator = self.do_find(search_sids, as_sid=as_sid)
        yield from generator

    @overload
    def do_find(self, search_sids: List[Sid], as_sid: Literal[True]) -> Iterator[Sid]:
        ...

    @overload
    def do_find(self, search_sids: List[Sid], as_sid: Literal[False]) -> Iterator[str]:
        ...

    @overload
    def do_find(
        self, search_sids: List[Sid], as_sid: Optional[bool]
    ) -> Iterator[Sid] | Iterator[str]:
        ...

    def do_find(
        self, search_sids: List[Sid], as_sid: Optional[bool] = True
    ) -> Iterator[Sid] | Iterator[str]:
        raise NotImplementedError(
            f"[Finder.do_find] is abstract, and seams not implemented. Class: {self.__class__}"
        )

    @overload
    def find_one(self, search_sid: str | Sid, as_sid: Literal[True]) -> Sid:
        ...

    @overload
    def find_one(self, search_sid: str | Sid, as_sid: Literal[False]) -> str:
        ...

    @overload
    def find_one(self, search_sid: str | Sid, as_sid: Optional[bool]) -> Sid | str:
        ...

    def find_one(self, search_sid: str | Sid, as_sid: Optional[bool] = True) -> Sid | str:
        """
        Returns the first Sid found using the given search_sid.

        Returns a Sid, if as_sid is True (default), or a Sid strings.

        Internally calls "first" on "find".

        Example:

            >>> from spil import FindInAll
            >>> FindInAll().find_one('hamlet/a/char/ophelia')
            Sid('asset__asset:hamlet/a/char/ophelia')

        Args:
            search_sid: typed or untyped Sid or string
            as_sid: if the result should be a Sid object or string

        Returns:
            first found Sid or string

        """
        found = first(self.find(search_sid, as_sid=False))  # read is faster if as_sid is False
        if as_sid:
            return Sid(found)
        else:
            return found

    def exists(self, search_sid: str | Sid) -> bool:
        """
        Returns True if the given search_sid returns a result.
        Else False.

        Internally calls "bool" on "find_one".

        Example:

            >>> from spil import FindInAll
            >>> FindInAll().exists('hamlet/a/char/ophelia')
            True

            >>> from spil import FindInAll
            >>> FindInAll().exists('hamlet/a/char/jimmy')
            False

        Args:
            search_sid: search_sid: typed or untyped Sid or string

        Returns:
            True if search_sid returns a result, else False
        """
        return bool(self.find_one(search_sid, as_sid=False))

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Finder())
