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

from spil import Sid, SpilException
from spil.conf import projects

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path


def sid_file_path():

    projects_root = Path(Sid(projects[0]).path).parent
    print('Root path : {}'.format(projects_root))

    sid_file = projects_root / 'sids.test.txt'

    if not projects_root.exists():
        raise SpilException('The root directory for Sids does not exist. Test aborted. See "project_root" in "fs_conf" configuration. Currently set to {}'.format(projects_root))

    return sid_file


def test_write_sids_file():

    sid_file = sid_file_path()

    from example_sids import sids  # generates the sids - potentially long loop

    with open(str(sid_file), 'w') as f:
        for sid in sids:
            f.write(str(sid) + '\n')

    print('Written Sids to {}'.format(sid_file))


if __name__ == '__main__':

    print('Generating Example Sids. This can take some time.')
    test_write_sids_file()
    print('Done.')