# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
To launch searches on LS, the saved Sid list.
(this list is either generated (see "save_sid_list_to_file"), or parsed (see "parse_sid_files")
 
Searches is a dict with searches as 
    key: search sid
    value: search description 

function: test_ls(searches) 
"""
import six

if six.PY3:  #TODO: add Timer in package for PY3 (they have a great package setup) - Also add tox.
    from codetiming import Timer
else:
    from spil_tests.mock_timer import Timer

from spil_tests.utils import init  # needs to be before spil.conf import
from spil import LS, FS
from spil_tests.prep.save_sid_list_to_file import sid_file_path


def test_ls_fs(searches):

    as_sid = False

    with open(str(sid_file_path()), 'r') as f:
        sids = f.read().splitlines()
    search_list = sids
    print('Searching in {} sids'.format(len(search_list)))

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
    print('Done all searches.')
    global_timer.stop()


if __name__ == '__main__':

    from spil.util.log import setLevel, ERROR, DEBUG
    setLevel(ERROR)

    searches = {}
    searches['FTOT/S/SQ0001/SH0010/*'] = ''

    test_ls_fs(searches)
