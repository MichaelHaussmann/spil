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

from spil.sid.sid import Sid
from spil.sid.read.util import first
from spil.sid.read.tools import unfold_search

from spil.util.log import debug, info, warning, error

class Finder:
    """
    Interface for Sid Finder.

    Implements common public Sid Search methods "find", "find_one", and "exists"
    """

    def __init__(self):
        pass

    def find(self, search_sid: str | Sid, as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        """
        gets the Sids found using the given search_sid.
        Returns a generator over Sids, if as_sid is True (default), or over Sid strings.

        The search process is as follows:
        - the search sid string is "unfolded" into a list of typed search Sids.
        - depending on the types of searches, defined by the search symbols ('>', ...), the search is delegated to a finder function.
        (currently either "sorted_search" or "star_search").

        :param search_sid: string or Sid
        :param as_sid:
        :return: Sid or string
        """
        # shortcut if Sid is not a search
        sid = Sid(search_sid)
        if sid and not sid.is_search():
            generator = self.do_find([sid], as_sid=as_sid)
        else:
            search_sids = unfold_search(search_sid)
            generator = self.do_find(search_sids, as_sid=as_sid)

        for i in generator:
            yield i

    def do_find(self, search_sids: List[Sid], as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        raise NotImplementedError(f"[Finder.do_find] is abstract, and seams not implemented. Class: {self.__class__}")

    def find_one(self, search_sid: str | Sid, as_sid: bool = True) -> Sid | str:
        """
        Returns the first Sid found using the given search_sid.

        Returns a Sid, if as_sid is True (default), or a Sid strings.

        Internally calls "first" on "find".

        :param search_sid: string
        :param as_sid:
        :return: Sid or string
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

        :param search_sid: string or Sid
        :return: True or False
        """
        return bool(self.find_one(search_sid, as_sid=False))

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Finder())
