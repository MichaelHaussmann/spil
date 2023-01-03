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
from typing import Optional, Mapping, Any
from spil import Sid

"""
As FindInAll, a configurable "WriteToAll" Writer is planned.
Note: if a FindInCache Finder is used, FindInCache.create() should also be a registered data destination.
"""


class Writer:
    """
    A "Writer" implements CRUD's Create/Update/Delete functions.

    The Writer creates Sids, with or without attributes.
    It Updates and Sets "data" / attributes for given Sids.
    It also deletes Sids.

    Writer is subclassed for the different data destinations,
    like the Filesystem or database management systems (WriteToPaths, WriteToShotgrid, etc.).

    WriteToPaths (as FindInPaths) works with Sids on the Filesystem.

    The goal of this CRUD formalisation is to propose a simple API around Sids.
    These features are still experimental.

    (Finders and Getters implement read)
    """

    def create(self, sid: Sid | str, data: Optional[dict] = None) -> bool:
        """
        Creates the given Sid, optionally with given data.

        Args:
            sid: Sid string or instance
            data: optional data dictionary

        Returns: True on success, False on failure
        """
        return False

    def update(self, sid: Sid | str, data: Mapping[str, Any]) -> bool:
        """
        Updates given data on given Sid.

        Args:
            sid: Sid string or instance
            data: data dictionary

        Returns: True on success, False on failure
        """
        return False

    def set(self, sid: Sid | str, attribute: Optional[str], value: Optional[Any], **kwargs) -> bool:
        """
        Sets given attribute with given value, and / or given kwargs, for given Sid.

        Args:
            sid: Sid string or instance
            attribute: attribute name, data key
            value: value for data
            **kwargs: key / value pairs.

        Returns: True on success, False on failure
        """
        return False

    def delete(self, sid: Sid | str) -> bool:
        """
        Deletes given Sid.

        Args:
            sid: Sid string or instance

        Returns: True on success, False on failure
        """
        return False

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Writer())
