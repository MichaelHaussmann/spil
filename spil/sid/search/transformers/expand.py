# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

from logging import FATAL
import string

import six

from spil.util.exception import SpilException
from spil.conf import sid_templates, sidtype_keytype_sep
from spil.sid.core.sid_resolver import sid_to_dict
from spil.sid.sid import Sid


def execute(sids):
    """
    Expands multi-search characters like /** into a series of /*.
    The ** must exist only once.
    If values are present after the ** they are supposed to be the end of the sids.

    :param sids:
    :return:
    """
    result = []
    for sid in sids:
        result.extend(expand(sid))

    return result


def expand(sid):  # FIXME: this code is slow and cryptic.

    # print 'DOING ' + sid

    if not sid.count('/**'):  # nothing to expand
        return [sid]

    if sid.count('/**') > 1:
        raise SpilException('Can only expand once in a Sid.')

    if sid.count('?'):  # sid contains URI ending. We put it aside, and later append it back
        sid, uri = sid.split('?', 1)
    else:
        uri = ''

    root = sid.split('/**')[0]
    _type = Sid(root).basetype
    if not _type:
        raise SpilException('The Search Sid "{}" is not typed, and cannot be expanded. This is probably a configuration error.'.format(sid))

    #print(Sid(root).type)
    #print (_type)
    found = []
    for key, template in six.iteritems(sid_templates):
        if key.startswith(_type + sidtype_keytype_sep):
            keys = list(string.Formatter().parse(template))
            if keys[-1][1] == 'ext':        # FIXME: hard coded
                count = len(keys)-1
                current = sid.count('/')
                needed = count-current+1
                #print needed
                test = sid.replace('/**', '/*' * needed)
                #print test
                __type, data = sid_to_dict(test)
                if data and (list(data)[-1] == 'ext'):  #
                    if uri:
                        test = '{}?{}'.format(test, uri)
                    found.append(test)
            else:
                break

    return set(found)


if __name__ == '__main__':

    from pprint import pprint
    from spil.util.log import setLevel, info

    info('Tests start')

    setLevel(FATAL)

    expandables = ['FTOT/S/*/**/ma', 'FTOT/A/**/V002/*/ma', 'FTOT', 'FTOT/A/**',
                   'FTOT/S/SQ0010/SH0010/ANI/**/abc',
                   'FTOT/S/**/mov',
                   'FTOT/S/SQ0010/SH0010/**/ma']

    expandables_with_uri = ['FTOT/S/*/**/ma?version=2', 'FTOT/A/**/V002/*/ma?whatever', 'FTOT', 'FTOT/A/**',
                   'FTOT/S/SQ0010/SH0010/ANI/**/abc',
                   'FTOT/S/**/mov',
                   'FTOT/S/SQ0010/SH0010/**/ma?yes?yes']

    for sid in expandables_with_uri:
        print(sid + '-->')
        results = expand(sid)
        for result in results:
            print(sid_to_dict(result))

        pprint(results)

        print('*'*10)
