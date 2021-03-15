# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.conf import extension_alias  # put into sid conf
from spil.conf import sip, ors


def execute(sids):
    """
    Maps extension aliases to a list of "or operator" separated extensions.

    Examples (with comma "," being the or-operator) :
         img -> jpg,exr,dpx
         hou -> hip, hipnc
         may -> ma, mb
    """
    result = []

    for sid in sids:
        result.append(extensions(sid))

    return result


def extensions(sid):

    parts = sid.split(sip)

    extension_part = parts[-1]
    # print 'extension_part', extension_part
    if extension_part.count(ors):
        extension_part = [x.strip() for x in extension_part.split(ors)]
    else:
        extension_part = [extension_part]

    #print 'extension_part', extension_part

    result = []
    for ext in extension_part:
        ext = extension_alias.get(ext, [ext])
        result.extend(ext)

    #print 'result', result
    sid = parts[:-1]
    sid.append(','.join(sorted(list(set(result)))))

    return sip.join(sid)




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

    for sid in expandables:
        print(sid + '-->' + str(extensions(sid)))

        print('*'*10)