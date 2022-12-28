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
from typing import Iterable, List, Set, Optional, Mapping, Any

"""
write.Writer

create Sids
update Sids
delete Sids
set attributes

The idea is to register data destinations, objects implementing Writer.
Eg. WriteTo

Note: if a FindInCache Finder is used, FindInCache.create() should also be a registered data destination.

(TBD:
WriteToDestinations
WriteToRegistered
WriteToMultiple... )
"""
from spil import Sid


class Writer:

    def create(self, sid: Sid | str, data: Optional[dict] = None) -> bool:
        """
        Creates the given Sid, with given data.

        :param sid: Sid or str
        :param data: dictionary
        :return: True on Success, False on failure
        """
        return False

    def update(self, sid: Sid | str, data: Mapping[str, Any]) -> bool:
        return False

    def set(self, sid: Sid | str, attribute: str, value: Optional[Any], **kwargs) -> bool:
        return False

    def delete(self, sid: Sid | str) -> bool:
        return False

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Writer())
