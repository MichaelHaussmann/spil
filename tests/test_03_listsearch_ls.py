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
from spil.util.log import info
from example_searches import searches

from tests.test_02_save_sids_to_file import sid_file_path


def test_ls(searches):

    do_doublon_check = True  # Set to false when testing performance
    as_sid = True

    with open(str(sid_file_path()), 'r') as f:
        sids = f.read().splitlines()
    search_list = sids
    info('Searching in {} sids'.format(len(search_list)))

    global_timer = Timer(name="global")
    global_timer.start()

    ls = LS(search_list, do_extrapolate=False, do_pre_sort=False)
    for search_sid, comment in six.iteritems(searches):

        print('*' * 10)
        print('{} --> {}'.format(search_sid, comment))
        double_check = set()

        ls_timer = Timer(name="search_sid")
        ls_timer.start()
        count = 0
        for i in ls.get(search_sid, as_sid=as_sid):
            print(i)
            count += 1
            if do_doublon_check:
                if i in double_check:
                    print('--------------------------------------> Doublon {}'.format(i))
                double_check.add(i)
            # sid = Sid(i)
            # print sid.path
        print('Total: ' + str(count))
        ls_timer.stop()
    global_timer.stop()


if __name__ == '__main__':

    from spil.util.log import setLevel, ERROR, DEBUG
    setLevel(DEBUG)

    test_ls(searches)
