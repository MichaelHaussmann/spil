"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Mapping, Any, Optional, List, Callable

import json

from spil.sid.read.getters.getter_finder import GetByFinder
from spil.util.log import warning, debug, error
from spil import Sid, FindInPaths
from spil.conf import default_path_config, path_data_suffix, get_data_json_path  # type: ignore


class GetFromPaths(GetByFinder):
    """
    Getter from File system.

    This is still experimental.
    """

    def __init__(self, config: Optional[str] = None):  # noqa
        self.config = config or default_path_config  # type: ignore
        self.finder = FindInPaths(config=config)

    def get_data(
        self, sid: str | Sid, attributes: Optional[List[str]] = None, sid_encode: Callable = str
    ) -> Mapping[str, Any]:
        """
        Returns data associated to the given Sid, as a key:value dictionary.
        Returns an empty dictionary if no data was found.

        Reads data dictionary from a json.
        To infer the jsons file path, the Sid path is used,
        with the suffix replaced, as per config.

        Args:
            sid:
            attributes:
            sid_encode:

        Returns: A key:value dictionary, or an empty dictionary
        """
        _sid = Sid(sid)
        sid_path = _sid.path(self.config)
        if not sid_path:
            debug(f'Given Sid "{sid}" has no path at config {self.config}. Cannot get data.')
            return {}
        data_path = get_data_json_path(sid_path)
        data: dict[str, Any] = {}
        if data_path.exists():
            try:
                with data_path.open() as f:
                    data = json.load(f) or {}
            except OSError as e:
                warning(f"Failed to open the json file. Sid: {sid}, file: {data_path}, Error: {e}")
            except json.JSONDecodeError as e:
                warning(f"Failed to decode Json. Sid: {sid}, file: {data_path}, Error: {e}")
            except Exception as e:
                warning(f"Failed to get data from json. Sid: {sid}, file: {data_path}, Error: {e}")

        encoded = sid_encode(_sid)
        if encoded:
            data["sid"] = encoded

        if attributes:
            return {key: data.get(key) for key in attributes}
        else:
            return data

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":
    from pprint import pprint

    print(GetFromPaths())
    search = "hamlet/a"

    print("Calling find:")
    for result in FindInPaths().find(search):
        pprint(result)

    print("Calling get:")
    for result2 in GetFromPaths().get(search, sid_encode=lambda x: x.uri):
        pprint(result2)

    print("Calling get with lambda None:")
    for result2 in GetFromPaths().get(search, sid_encode=lambda x: None):
        pprint(result2)

    print(GetFromPaths().get_attr(search, "bill"))
