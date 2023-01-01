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
from typing import Iterator, Mapping, Any, Optional

from pathlib import Path
import json

from spil import Sid, Getter, FindInPaths
from spil.conf import default_path_config, path_data_suffix  # type: ignore

from spil.sid.read.util import first


def _read_data(sid_path: Path) -> dict:
    """
    Reads data dictionary from json.
    To get the jsons file path, the suffix is replaced, as per config.

    Args:
        sid_path: path from a valid sid

    Returns: data dictionary
    """
    # TODO: add Exception handling

    data_path = sid_path.with_suffix(path_data_suffix)
    data: dict[str, Any] = {}
    if data_path.exists():
        with open(data_path) as f:
            data = json.load(f) or dict()
    return data


class GetFromPaths(Getter):
    """
    Getter from File system.

    This is still experimental.
    """

    def __init__(self, config: Optional[str] = None):
        self.config = config or default_path_config  # type: ignore
        self.finder = FindInPaths(config=config)

    def get(self, search_sid: str | Sid, attribute: Optional[str] = None, as_sid: bool = False) -> Iterator[Mapping[str | Sid, Any | dict]]:
        """
        For a given search, returns an Iterator over Mappings containing a Sid as key,
        and the retrieved data as value.

        By default, attribute is None, retrieved data is a dictionary containing all configured data for the Sid type.
        If attribute is given, data contains only the value of the given attribute.

        The Sids returned by Getter.get() are identical to those returned by Finder.find().
        Getter retrieves data related to these Sids, whereas the Finder only the existing Sids themselves.

        Args:
            as_sid:
            search_sid:
            attribute:

        Returns:
            An iterator over Mappings containing a Sid as key,
            and the retrieved data as value. Either for a given attribute (attribute),
            or all data in a dictionary (data as configured).

        """
        for sid in self.finder.find(search_sid=search_sid, as_sid=True):
            data = _read_data(sid.path(self.config))
            if not as_sid:
                sid = str(sid)  # type: ignore  # (redefining sid as str)
            if attribute:
                yield {sid: data.get(attribute)}
            else:
                yield {sid: data}

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":
    from pprint import pprint
    print(GetFromPaths())
    search = 'vic/a'
    for result in FindInPaths().find(search):
        pprint(result)
    for result in GetFromPaths().get(search):
        pprint(result)

    print(GetFromPaths().get_attr(search, 'bill'))