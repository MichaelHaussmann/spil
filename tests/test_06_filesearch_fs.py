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
from spil import FS
from spil.util.log import debug, setLevel, INFO, DEBUG, info
from example_searches import searches

#searches = {}
searches['raj/a/location/?/**/maya'] = 'All sets that have maya files'
searches['raj/s/sq001/**/>/>/p/avi'] = 'All sets that have maya files'

def test_fs():

    do_doublon_check = True  # Set to false when testing performance

    global_timer = Timer(name="global")
    global_timer.start()

    ls = FS()
    for search_sid, comment in six.iteritems(searches):

        print('*' * 10)
        print('{} --> {}'.format(search_sid, comment))
        double_check = set()

        ls_timer = Timer(name="search_sid")
        ls_timer.start()
        for i in ls.get(search_sid):
            print(i)
            if do_doublon_check:
                if i in double_check:
                    print('--------------------------------------> Doublon {}'.format(i))
                double_check.add(i)
            # sid = Sid(i)
            # print sid.path
        ls_timer.stop()
    global_timer.stop()


if __name__ == '__main__':

    setLevel(INFO)
    test_fs()
