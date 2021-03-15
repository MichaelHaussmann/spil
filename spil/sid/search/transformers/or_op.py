# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.conf import sip, ors


def execute(sids):
    """

    :param sids:
    :return:
    """
    result = []
    for sid in sids:
        result.extend(or_op(sid))

    return result


def or_op(sid):

    if not sid.count(ors):  # no "or" operators in sid.
        return [sid]

    _start = '--start--'

    parts = sid.split(sip)

    found = [_start]
    for part in parts:
        #print part
        current = found[:]
        if ors in part:
            for alt in part.split(ors):
                alt = alt.strip()
                for sid in current[:]:
                    new = sid + sip + alt
                    #print 'replace', sid, ' --> ', new, ' -- ', sid in found, '?'
                    #
                    if sid in found:
                        found[found.index(sid)] = new  # replace (of the first element)
                    else:
                        found.append(new)  # replace (of the first element)

            # found.remove()
        else:
            for sid in found[:]:
                new = sid + sip + part
                # print new
                found[found.index(sid)] = new  # replace (of the first element)

    result = []
    for sid in found:
        if not sid in result:
            result.append(sid.replace(_start + sip, ''))

    # no type check needed
    return result


if __name__ == '__main__':

    from pprint import pprint
    from spil.util.log import setLevel, INFO, info

    info('Tests start')

    setLevel(INFO)

    tests = ['aral/s/s010,s020/*/**/mb,nk,ma']

    for sid in tests:
        print(sid + '-->')
        results = or_op(sid)
        pprint(results)

        print('*'*10)