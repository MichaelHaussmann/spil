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
from typing import Iterable, List, Set, Optional

import shutil

from spil import Sid, SpilException, Writer
from spil.conf import default_path_config, create_file_using_template, create_file_using_touch
from spil.util.log import debug
from pathlib import Path


def _create_parent(path: Path) -> bool:

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    return path.parent.exists()


class WriteToPaths(Writer):

    def __init__(self, config: Optional[str] = None):
        self.config = config or default_path_config  # type: ignore

    def create(self, sid: Sid | str, data: dict | None = None) -> bool:

        _sid = Sid(sid)
        if not _sid.path(self.config):
            raise SpilException(f"[WriteToPaths] Cannot Create: sid {sid} has no path (config: {self.config}).")

        path = _sid.path(self.config)
        if path.exists():
            raise SpilException(f"[WriteToPaths] Cannot Create: path already exists for {sid}. Path: {path} (config: {self.config}).")

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

        return path.exists()

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":
    print(WriteToPaths())

