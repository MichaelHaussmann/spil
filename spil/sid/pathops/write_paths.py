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

import shutil
import json

from spil import Sid, Writer
from spil.util.exception import SpilException
from spil.conf import default_path_config, create_file_using_template, create_file_using_touch, get_data_json_path  # type: ignore
from spil.util.log import debug, warning, error
from pathlib import Path


def _create_parent(path: Path) -> bool:
    """
    Creates parent folder(s) of given Path.

    Args:
        path: path for which parent should be created.

    Returns: True on success, False on failure.
    """

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    return path.parent.exists()


def _write_data(sid_path: Path, data: Mapping[str, Any]) -> bool:
    """
    Writes given data to json.
    To get the jsons file path, the suffix is replaced, as per config.

    If the json already exists, it is loaded, updated, and dumped.
    Else the json is created.

    Args:
        sid_path: path from a valid sid
        data: data dictionary

    Returns: True on success, False on failure
    """

    data_path = get_data_json_path(sid_path)

    try:
        # if there is already data, we load and update it
        if data_path.exists():
            with data_path.open() as f:
                previous_data = json.load(f) or {}
                previous_data.update(data)
                data = previous_data

        # dumping data, converting to string if not serializable
        data_path.write_text(json.dumps(data, indent=4, default=str))

        return data_path.exists()

    except json.JSONDecodeError as e:
        error(f"Could not decode json at {sid_path}. Error: {e}")
        raise
        # return False

    except OSError as e:
        error(f"Could not access the json file {sid_path}. Error: {e}")
        raise
        # return False

    except Exception as e:
        error(f"Unexpected exception saving data at {sid_path}. Error: {e}")
        raise
        # return False


class WriteToPaths(Writer):
    """
    Writer to Paths.
    "Writers" implement the CRUD's Create/Update/Delete functions.

    WriteToPaths edits Sids and Sid data at the file system.

    This class should be considered an example implementation.
    Although it can be considered useful, it is not by itself production ready.
    It is used to create mock/test files and folders for Sid testing purposes.

    As FindInPaths and the sid.path() it is possible to instantiate this Writer with a fs config name.
    The config name points to the path templates config file.

    Sids are created at the configured path.
    Sid File creation is either done by copy of a template file (if exists as configured),
    or by "touch", which creates an empty file.

    Data is created and updated in the form of a json file, at the same path, with a specific configured suffix.
    """

    def __init__(self, config: Optional[str] = None):
        self.config = config or default_path_config  # type: ignore

    def create(self, sid: Sid | str, data: Optional[dict] = None) -> bool:

        _sid = Sid(sid)
        if not _sid.path(self.config):
            raise SpilException(
                f"[WriteToPaths] Cannot Create: sid {sid} has no path (config: {self.config})."
            )

        path = _sid.path(self.config)
        if path.exists():
            raise SpilException(
                f"[WriteToPaths] Cannot Create: path already exists for {sid}. Path: {path} (config: {self.config})."
            )

        suffix = path.suffix
        if suffix:
            debug(f"Path is a file: {path}")
            template = create_file_using_template.get(suffix[1:])  # we remove the dot of the suffix
            if template:
                debug(f"Will be created by copying template: {template}")
                _create_parent(path)
                shutil.copy2(template, path)
            elif create_file_using_touch:
                debug(f"Will be created by touch. {path}")
                _create_parent(path)
                path.touch()
            else:
                debug(f"File will not be created: {path}")

        else:
            debug(f"Path is a directory {path}")
            path.mkdir(parents=True)

        if not path.exists():
            warning(f"Creation of {sid} has failed. Path was not created: {path}")
            return False

        # Now creating optional data
        if data:
            return _write_data(path, data)

        return path.exists()

    def update(self, sid: Sid | str, data: Mapping[str, Any]) -> bool:
        """
        Updates given data on given Sid.

        Args:
            sid: Sid string or instance
            data: data dictionary

        Returns: True on success, False on failure
        """
        _sid = Sid(sid)
        if not _sid.path(self.config):
            raise SpilException(
                f"[WriteToPaths] Cannot update: sid {sid} has no path (config: {self.config})."
            )

        path = _sid.path(self.config)
        if not path.exists():
            raise SpilException(
                f"[WriteToPaths] Cannot Update: Sid {sid} does not exist at path: {path} (config: {self.config})."
            )

        return _write_data(path, data)

    def set(
        self, sid: Sid | str, attribute: Optional[str] = None, value: Optional[Any] = None, **kwargs
    ) -> bool:
        """
        Sets given attribute with given value, and / or given kwargs, for given Sid.
        Updates the data if it already exists.

        Internally calls update().

        Args:
            sid: Sid string or instance
            attribute: attribute name, data key
            value: value for data
            **kwargs: key / value pairs.

        Returns: True on success, False on failure
        """
        if attribute:
            kwargs[attribute] = value
        return self.update(sid, data=kwargs)

    def delete(self, sid: Sid | str) -> bool:
        raise NotImplementedError("Deletion is currently not implemented.")

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":

    sid = "hamlet/a"
    data = {"author": "John"}
    print(WriteToPaths())
    writer = WriteToPaths()
    done = writer.update(sid, data)
    print(Sid(sid).path())
    print(f"Update: {done}")

    done = writer.set(sid, bill=25, random_attribute="random value")
    print(f"Set: {done}")

    done = writer.set(sid, attribute="bill", value=299)
    print(f"Set: {done}")
