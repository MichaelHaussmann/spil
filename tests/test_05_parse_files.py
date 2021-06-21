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
from tests import test_00_init  # needs to be before spil.conf import

from spil.util.log import debug, setLevel, INFO, DEBUG, info
from spil import Sid, SpilException
from spil.conf import projects

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

from tests.test_02_save_sids_to_file import sid_file_path


def test_parse_files():

    sid_file = sid_file_path().parent / 'sids.parsed.txt'

    if sid_file.exists():
        raise SpilException('The parse file "{}" already exists. Skipped'.format(sid_file))

    for project in projects[:]:

        project_root = Path( Sid(project).path )
        print('Root path : {}'.format(project_root))

        with open(str(sid_file), 'a') as f:

            for path in project_root.rglob('*'):
                if path.name.startswith('.') or path.name.startswith('_'):
                    continue
                if path.suffix in ['.png', '.exr', '.jpg', '.raysync']:  # currently not supported - speed up parsing
                    continue
                print(path)
                sid = Sid(path=path)
                if str(sid):
                    f.write(str(sid) + '\n')


if __name__ == '__main__':

    setLevel(INFO)  # Set to ERROR if file system contains a lot of non Sid translatable files.

    test_parse_files()

