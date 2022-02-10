# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import six
from spil_tests.utils import init  # needs to be before spil.conf import

from spil.util.log import debug, setLevel, INFO, DEBUG, info, ERROR
from spil import Sid, SpilException
from spil.conf import projects

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path


def is_ok(path):
    """
    Quick filter function to speed up parsing.
    """
    if not (str(path).count('3_PROD') or str(path).count('4_POSTPROD')):
        return False
    if path.name.startswith('.') or path.name.startswith('_') or path.suffix.endswith('~'):
        return False
    if path.suffix in ['.png', '.exr', '.jpg', '.raysync', '.swatches', '.comment']:  # currently not supported - speed up parsing
        if not (str(path).count('.0100.') or str(path).count('.0101.')):  # we keep first frames only
            return False
    if str(path).count(r'\.') or str(path).count(r'\_'):
        return False
    return True


def test_parse_files(sid_file, is_ok_callback=None):
    """
    Recursively traverses the project directories, and fetches all compatible Sids into a file.

    is_ok_callback is a function to filter out paths that do not need to be Sid tested.
    """

    print('Sids will be written to : {}'.format(sid_file))

    if is_ok_callback:
        is_ok = is_ok_callback
    else:
        def is_ok(path):
            return True

    if sid_file.exists():
        raise SpilException('The parse file "{}" already exists. Skipped'.format(sid_file))

    for project in projects[:]:

        project_root = Path( Sid(project).path )
        print('Root path : {}'.format(project_root))

        with open(str(sid_file), 'a') as f:

            for path in project_root.rglob('*'):
                if not is_ok(path):
                    continue
                print(path)
                sid = Sid(path=path)
                if str(sid):
                    f.write(str(sid) + '\n')


if __name__ == '__main__':

    setLevel(ERROR)  # Set to ERROR if file system contains a lot of non Sid translatable files.
    from spil_tests.utils.save_sid_list_to_file import sid_file_path

    sid_file = sid_file_path().parent / 'sids.parsed.txt'
    test_parse_files(sid_file)

