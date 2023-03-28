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
from typing import Iterable, List, Set, Optional, Mapping, Any


# FIXME: This is work in progress.

from spil import Sid, Writer
# from spil.conf import get_creator, get_updater, get_setter, get_deleter


class WriteToAll(Writer):
    """
    This Writer is a thin layer to delegate all Write operations to configured functions.
    This allows existing or external pipeline write functions to be wrapped by a Writer, without the need to implement one.

    Note that it is recommended to implement a custom writer, because the code is better structured,
    but this approach is not always possible or desirable.
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
    print(WriteToAll())
