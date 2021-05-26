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
from tests import test_00_init  # import needed before spil.conf

from spil.conf import sid_templates, path_templates
from spil.util.log import info
from warnings import warn

from example_sids import sids  # generates the sids - potentially long loop
from pprint import pprint

print(test_00_init)


def test_sids(sids):

    info('Testing if example sids match the Sid config')

    if not sids:
        warn('No sids given, nothing to test.')
        return

    for s in sids:
        info('----------------')
        info('Testing: "{}"'.format(s))
        sid = Sid(s)
        assert sid.string == s

        if not sid.type:
            warn('Sid "{}" not typed, skipping'.format(sid))
            continue

        key = sid.keytype
        parent_key = sid.parent.keytype

        assert sid.parent == sid.get_as(parent_key)

        if not sid.get_last(key):
            warn('Sid "{}" does not return get_last("{}") - probably bad.'.format(sid, key))

        params = {'parent': sid.parent,
                  'grand_parent': sid.parent.parent,
                  'basetype': sid.basetype,
                  'keytype': sid.keytype,
                  'path': sid.path,
                  'exists': sid.exists(),
                  'is_leaf': sid.is_leaf(),
                  'len': len(sid),
                  'get_last': sid.get_last(key)
                  }

        pprint(params)


if __name__ == '__main__':

    print()
    print('Sid test starts')

    bad_sids = ['FTOT', 'FTOT/A/CHR/COCOi', 'FTOT/A/CHR/COCO-2', 'FTOT/A/CHR/COCO-32',  'FTOT/A/CHR/COCO25']
    # test_sids(bad_sids)

    # to test "get_last" on tasks, seq and shots
    specific_sids = ['FTOT/A/CHR/TEST/MOD', 'FTOT/S/SQ0001/SH0010/LAY', 'FTOT/S/SQ0001/SH0010', 'FTOT/S/SQ0001']  # , 'FTOT/A/CHR/TEST/MOD/V001/WIP', 'FTOT/S/SQ0001/SH0020/LAY/V001']
    test_sids(specific_sids)

    # bugged "get_last" on versions / state
    specific_sids = ['FTOT/A/CHR/TEST/MOD/V001/WIP', 'FTOT/S/SQ0001/SH0020/LAY/V001']
    test_sids(specific_sids)

    #test_sids(sids[:5000])

    print('Done')



