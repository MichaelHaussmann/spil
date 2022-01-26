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
    from spil_tests.mock_timer import Timer

from spil_tests import test_00_init  # needs to be before spil.conf import
from spil import FS
from spil.util.log import info
from example_searches import searches


def test_fs(searches):

    do_doublon_check = True  # Set to false when testing performance
    as_sid = True

    global_timer = Timer(name="global")
    global_timer.start()

    ls = FS()
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
    setLevel(ERROR)

    #searches = {}
    # searches['CBM/*'] = ''
    # searches['CBM/S/*'] = ''
    # searches['CBM/S/SQ0001/*'] = ''
    searches['FTOT/S/SQ0001/SH0010/*'] = ''
    # searches['FTOT/S/SQ0001/SH0020/COMPO/**'] = ''
    #searches['CBM/S/SQ0001/SH0020/**'] = ''
    #searches['CBM/S/SQ0001/SH0020/**/nk'] = ''
    # searches['CBM/S/SQ0001/SH0020/COMPO/*/nk'] = ''
    # searches['CBM/S/SQ0001/SH0020/*/*/nk'] = ''
    #searches['CBM/S/SQ0001/SH0020/COMPO/v001/nk'] = ''

    test_fs(searches)

    """
    Problem:
    
    FTOT/S/SQ0001/SH0020/ANI/**/cache,maya?state=WIP&version=>
    Doesn't return FTOT/S/SQ0001/SH0020/ANI/V019/WIP/CAM/abc
    Reason: General "sort by / group by" problem.
    Missing a "sort by row".
    Now just makes an overall sort and group by the previous to ">" field.
    So it is the "last" version, but across all states, extensions, etc. Not what we would expect if we do a broad search.

    """