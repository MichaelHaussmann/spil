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

if six.PY3:  #TODO: add Timer in package for PY3 (they have a great package setup) - Also add tox.
    from codetiming import Timer
else:
    from tests.mock_timer import Timer

from tests import test_00_init  # needs to be before spil.conf import
from spil import LS
from spil import FS
from spil.util.log import debug, setLevel, INFO, DEBUG, info
from example_searches import searches

from tests.test_02_save_sids_to_file import sid_file_path


def test_ls_fs():

    with open(str(sid_file_path()), 'r') as f:
        sids = f.read().splitlines()

    search_list = sids
    info('Searching in {} sids'.format(len(search_list)))

    as_sid = False

    global_timer = Timer(name="global")
    global_timer.start()

    ls = LS(search_list, do_extrapolate=False, do_pre_sort=False)
    fs = FS()
    for search_sid, comment in six.iteritems(searches):

        print('*' * 10)
        print('{} --> {}'.format(search_sid, comment))

        ls_timer = Timer(name="ls_timer")
        ls_timer.start()
        found_ls = set(ls.get(search_sid, as_sid=as_sid))
        print('LS : {}'.format(len(found_ls)))
        ls_timer.stop()

        fs_timer = Timer(name="fs_timer")
        fs_timer.start()
        found_fs = set(fs.get(search_sid, as_sid=as_sid))
        print('FS : {}'.format(len(found_fs)))
        fs_timer.stop()

        problems = found_fs ^ found_ls

        for i in problems:
            print('Problem: {}'.format(i))

    print('*' * 10)
    info('Done all searches.')
    global_timer.stop()


if __name__ == '__main__':

    setLevel(INFO)
    test_ls_fs()
