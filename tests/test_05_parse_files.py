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

from spil import Sid
from spil.conf import projects

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

from tests.test_02_save_sids_to_file import sid_file_path


def test_parse_files():

    sid_file = sid_file_path().parent / 'sids.parsed.txt'

    for project in projects:

        project_root = Path( Sid(project).path )
        print('Root path : {}'.format(project_root))

        with open(str(sid_file), 'w') as f:

            for path in project_root.rglob('*'):
                print(path)
                sid = Sid(path=path)
                if str(sid):
                    f.write(str(sid) + '\n')


if __name__ == '__main__':

    test_parse_files()

