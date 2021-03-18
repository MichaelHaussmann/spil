# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import os
import six

from spil import Sid
from spil.util.utils import is_filename

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

from tests.test_02_save_sids_to_file import sid_file_path


def test_generate_files(max_amount=100000):

    test_paths = []

    with open(str(sid_file_path()), 'r') as f:
        sids = f.read().splitlines()

    # if not input('Create if not existing ?'):
    # sys.exit()

    for test in sids[:max_amount]:

        sid = Sid(test)
        # print('Sid : {}'.format(sid))

        """
        # We fill defaults, and strip
        sid.set_defaults()
        print('Sid with defaults: {}'.format(sid))
        sid = sid.get_stripped()
        print('Sid stripped: {}'.format(sid))
        """

        path = sid.path
        if path:
            path = Path(path)
            # print(path)
            if not path.exists():
                if is_filename(path):
                    # print(path, 'is a file')
                    if not path.parent.exists():
                        os.makedirs(str(path.parent))
                    path.touch()
                else:
                    # print(path, 'is a dir')
                    os.makedirs(str(path))

                print('Created test path: {}'.format(path))


if __name__ == '__main__':

    from spil.util.log import setLevel, INFO, WARN

    print('')
    print('Tests start')
    print('')

    # setLevel(WARN)
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    print('*' * 60)

    test_generate_files(100000)

