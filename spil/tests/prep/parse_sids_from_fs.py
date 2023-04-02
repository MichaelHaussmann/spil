# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

# from tests.utils import init  # needs to be before spil.conf import

from spil.util.log import debug, info
from spil import Sid
from spil.conf import projects  # type: ignore

from pathlib import Path


def is_ok(path):
    """
    Quick filter function to speed up parsing.
    """
    if path.name.startswith('.') or path.name.startswith('_') or path.suffix.endswith('~'):
        return False
    if path.suffix in ['.png', '.exr', '.jpg', '.raysync', '.swatches', '.comment']:  # currently not supported - speed up parsing
        return False
    return True


def parse_sids_from_files(filter_callback=None, config=None):
    """
    Recursively traverses the project directories, fetches and yields all compatible Sids.

    config is the Spil path config to be used when instantiating Sids.
    If None, the default config is used.

    is_ok_callback is a function to filter out paths that do not need to be Sid tested.

    Args:
        filter_callback: function that returns False if the path should be ignored, else True.
        config:

    Returns:

    """
    if filter_callback:
        is_ok = filter_callback
    else:
        def is_ok(path):
            return True

    for project in projects[:]:

        project_root = Path(Sid(project).path(config))
        info('Root path : {}'.format(project_root))

        for path in project_root.rglob('*'):
            if not is_ok(path):
                continue
            debug(path)
            sid = Sid(path=path, config=config)
            if str(sid):
                yield sid


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, INFO, ERROR

    setLevel(ERROR)  # Set to ERROR if file system contains a lot of non Sid translatable files.

    generator = parse_sids_from_files(filter_callback=is_ok)

    for sid in generator:
        print(f"Found: {sid} \t @ \t {sid.path()}")
