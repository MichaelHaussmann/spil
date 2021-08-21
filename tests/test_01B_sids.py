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
from tests import test_00_init  # import needed before spil.conf

from spil.util.log import debug, setLevel, INFO, DEBUG, info, ERROR, error

from spil.conf import sid_templates, path_templates
from spil.util.log import info
from warnings import warn

from example_sids import sids  # generates the sids - potentially long loop
from pprint import pprint, pformat

print(test_00_init)


def test_sids(sids, reraise=True):

    info('Testing if example sids match the Sid config')

    if not sids:
        warn('No sids given, nothing to test.')
        return

    for i, s in enumerate(sids):
        print('---------------- {}'.format(i))
        print('Testing: "{}"'.format(s))
        sid = Sid(s)
        print('Instanced: "{}"'.format(sid.full_string))

        if not s.count('?'):  # Asset works only without URI part
            assert str(sid) == s
        assert sid == eval(repr(sid))

        try:
            assert sid == Sid(sid.get('project') + '?' + sid.get_uri())

            if not sid.type:
                warn('Sid "{}" not typed, skipping'.format(sid))
                continue

            key = sid.keytype
            parent_key = sid.parent.keytype

            if not sid.type == 'project':
                if not sid.parent == sid.get_as(parent_key):
                    warn('Sid "{}" parent problem'.format(sid))

            if not sid.get_last(key):
                print('Sid "{}" does not return get_last("{}") - probably bad.'.format(sid, key))

            path = sid.path
            if path:
                assert sid == Sid(path=sid.path)
                assert sid.path == Sid(path=sid.path).path
            else:
                print('Sid "{}" has no path.'.format(sid))

            params = {'parent': sid.parent,
                      'grand_parent': sid.parent.parent,
                      'basetype': sid.basetype,
                      'keytype': sid.keytype,
                      'path': sid.path,
                      'exists': sid.exists(),
                      'is_leaf': sid.is_leaf(),
                      'len': len(sid),
                      'get_last': sid.get_last(key),
                      'get_next': sid.get_next('version'),
                      'get_new': sid.get_new('version'),
                      'type': sid.type,
                      'full_string': sid.full_string,
                      'string': sid.string,
                      'uri': sid.get_uri(),
                      }

            pprint(params)
            pprint(sid.data)

        except SpilException as e:
            error('SpilException : {} --> {}'.format(e, s))
            if reraise:
                raise e

        except Exception as e:
            error('Exception : {} --> {}'.format(e, s))
            if reraise:
                raise e


if __name__ == '__main__':

    setLevel(ERROR)

    print()
    print('Sid test starts')

    bad_sids = [ 'FTOT/A/CHR/COCOi', 'FTOT/A/CHR/COCO 2', 'FTOT/A/CHR/COCO_2', 'FTOT/A/CHR/COCO-32',  'FTOT/A/CHR/COCO25'] # 'FTOT',
    # test_sids(bad_sids)

    # to test "get_last" on tasks, seq and shots
    specific_sids = ['FTOT/A/CHR/TEST/MOD', 'FTOT/S/SQ0001/SH0010/LAY', 'FTOT/S/SQ0001/SH0010', 'FTOT/S/SQ0001']  # , 'FTOT/A/CHR/TEST/MOD/V001/WIP', 'FTOT/S/SQ0001/SH0020/LAY/V001']
    # test_sids(specific_sids)

    # bugged "get_last" on versions / state
    specific_sids = ['FTOT/S/SQ0001/SH0020/LAY/V001', 'FTOT/A/CHR/TEST/MOD/V001/WIP']
    # test_sids(specific_sids)

    data_sids = ['FTOT/S/SQ0001/SH0010/CASTING', 'FTOT/S/SQ0001/SH0010/FRAMERANGE', 'FTOT/S/SQ1000/SH0010/CASTING']
    #test_sids(data_sids)

    working_uri = ['FTOT?type=A', 'FTOT?type=A&cat=PRP', 'FTOT?type=A?cat=PRP']

    failing_uri = ['THING?type=A&cat=PRP', 'FTOT?cat=PRP' ]

    #test_sids(working_uri)
    # test_sids(failing_uri)

    test_sids(sids[:5000])

    new_tasks = ['FTOT/S/SQ0001/SH0020/FX-*', 'FTOT/S/SQ0001/SH0020/*', 'FTOT/S/SQ0001/SH0020/FX', 'FTOT/S/SQ0001/SH0020/FX-MOCCO']
    # test_sids(new_tasks)

    bad_tasks = ['FTOT/S/SQ0001/SH0020/F', 'FTOT/S/SQ0001/SH0020/FXMOCCO', 'FTOT/S/SQ0001/SH0020/RND-']
    # test_sids(bad_tasks, reraise=False)

    new_tasks = ['FTOT/A/CHR/MOCCO/CFXin', 'FTOT/A/CHR/MOCCO/CFXsim', 'FTOT/A/CHR/MOCCO/CFXsim-HAT',]
    test_sids(new_tasks)

    bad_tasks = ['FTOT/S/SQ0001/SH0020/F', 'FTOT/S/SQ0001/SH0020/FXMOCCO', 'FTOT/S/SQ0001/SH0020/RND-']
    # test_sids(bad_tasks, reraise=False)

    print('Done')



