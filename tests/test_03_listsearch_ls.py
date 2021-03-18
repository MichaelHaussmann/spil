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
from spil import LS
from spil.util.log import debug, setLevel, INFO, DEBUG, info
from example_searches import searches

from tests.test_02_save_sids_to_file import sid_file_path


def test_ls():

    with open(str(sid_file_path()), 'r') as f:
        sids = f.read().splitlines()

    search_list = sids
    info('Searching in {} sids'.format(len(search_list)))

    ls = LS(search_list, do_extrapolate=False)
    for search_sid, comment in six.iteritems(searches):
        print('*'*10)
        print('{} --> {}'.format(search_sid, comment))
        double_check = set()
        for i in ls.get(search_sid):
            print(i)
            if i in double_check:
                print('--------------------------------------> Doublon {}'.format(i))
            double_check.add(i)
            # sid = Sid(i)
            # print sid.path


if __name__ == '__main__':

    setLevel(INFO)

    test_ls()




