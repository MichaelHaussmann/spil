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

from spil.conf import sid_templates
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
        raise Exception('Can only expand once in a Sid.')

    root = sid.split('/**')[0]
    _type = Sid(root).keytype.split('__')[0]  # FIXME: Sid concept of root type
    #print(Sid(root).type)
    #print (_type)
    found = []
    for key, template in six.iteritems(sid_templates):
        if key.startswith(_type + '__'):
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
                    found.append(test)
            else:
                break

    return set(found)


if __name__ == '__main__':

    from pprint import pprint
    from spil.util.log import setLevel, info

    info('Tests start')

    setLevel(FATAL)

    expandables = ['aral/s/*/**/ma', 'aral/i/**/p/*/exr', 'aral', 'aral/a/**',
                   'aral/i/s010/p010/animation/**/exr',
                   'aral/i/**/exr',
                   'aral/i/s010/p010/**/exr']

    for sid in expandables:
        print(sid + '-->')
        results = expand(sid)
        for result in results:
            print(sid_to_dict(result))
        pprint(results)

        print('*'*10)
