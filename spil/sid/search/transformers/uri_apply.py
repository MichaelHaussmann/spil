# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil import Sid


def execute(sids):
    """
    Sids contain a URI at the end:
    eg,
    """
    result = []

    for sid in sids:
        done = uri_apply(sid)
        if done:
            result.append(done)

    return result


def uri_apply(sid):

    if not sid.count('?'):  # no uri
        return sid

    new_sid, uri = sid.split('?', 1)

    new_sid = Sid(new_sid)

    if not new_sid:  # sid is not typed - we cannot bake the uri
        return None

    uri = uri.replace('?', '&')  # we allow ?a=b?x=y but change it to a proper uri: ?a=b&x=y

    uri_pairs = {}
    for item in uri.split('&'):
        key, value = item.split('=')
        uri_pairs[key] = value

    # print(uri_pairs)

    new_sid = new_sid.get_with(**uri_pairs)

    if new_sid:
        return new_sid.string
    else:
        return None


if __name__ == '__main__':

    from spil.util.log import setLevel, info
    from logging import FATAL

    info('Tests start')

    setLevel(FATAL)

    expandables = ['aral/s/*/hou',
                   'aral/s/*/p/*/exr,img, hou',
                   'aral',
                   'aral/a/*/img',
                   'aral/s/s010/p010/animation/*/v001/p/vdb',
                   'aral/s/*/movie',
                   'aral/s/s010/p010/**/exr']

    working = ['FTOT?type=A',
                   'FTOT?type=A&cat=PRP'
                   'FTOT?type=A?cat=PRP']

    failing = ['THING?type=A&cat=PRP',
               'FTOT?cat=PRP',
    ]

    for sid in working + failing:
        print(sid + ' --> ' + str(uri_apply(sid)))

        print('*'*10)