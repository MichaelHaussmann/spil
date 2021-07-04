# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""


import string

import six

from spil.util.log import info, debug
from spil.util.exception import SpilException
from spil.conf import sid_templates, sidtype_keytype_sep
from spil.sid.core.sid_resolver import sid_to_dicts
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


def expand(sid, do_extrapolate=False):
    """
    This expects a string and converts to Sid (#SMELL)

    "Expand" means replacing a double wildcard "/**" by the possible amount of simple wildcards "/*", wherever possible.
    This allows for simpler searches on multiple types.

    Example:
        To find all movie files from a shot, we need to search for: FTOT/S/SQ0001/SH0020/*/*/*/mov
        FTOT/S/SQ0001/SH0020/**/mov is a simpler form.


    By default, expand only returns leaf types (do_extrapolate=False)
    FTOT/S/SQ0001/SH0020/** will be expanded to files, eg FTOT/S/SQ0001/SH0020/*/*/*/* and FTOT/S/SQ0001/SH0020/*/*/*/*/*

    If do_extrapolate is True, expand will return all possible intermediate types.
    Eg. FTOT/S/SQ0001/SH0020/** will also be expanded to FTOT/S/SQ0001/SH0020 (shot), and FTOT/S/SQ0001/SH0020/* (task), etc.
    This is not the default behaviour.


    The expand works like this:
    - First we get the root of the given Sid, before the "/**". We get the roots basetype ("asset", or "shot", etc).

    - Then we look up all existing types (sid_templates), until we match the basetype.
    For this type, we know the amount of keys, and replace "/**" by "/*" x the amount of keys.
    That gives us a test sid, that we use to instantiate valid sids, using all possible templates again.

    - we continue with all the types we have not already tested.

    """

    debug('Expanding ' + sid)
    sid = str(sid)

    if not sid.count('/**'):  # nothing to expand
        r = set([Sid(sid)])
        debug('Nothing to expand for {}. Just casting to Sid set {}'.format(sid, r))
        return r

    if sid.count('/**') > 1:
        raise SpilException('Can only expand once in a Sid.')

    if sid.count('?'):  # sid contains URI ending. We put it aside, and later append it back
        sid, uri = sid.split('?', 1)
    else:
        uri = ''

    root = sid.split('/**')[0]
    basetype = Sid(root).basetype
    if not basetype:
        raise SpilException('The Search Sids "{}" root "{}" cannot be typed, so it cannot be expanded. This is probably a configuration error.'.format(sid, root))

    tested = []
    found = []
    result = []
    for key, template in six.iteritems(sid_templates):
        debug('Checking ' + key)
        if key in found:
            debug('Already checked, continue')
            continue
        if key.startswith(basetype + sidtype_keytype_sep):  # matching basetype
            debug('Matching basetype "{}" for key "{}"'.format(basetype, key))
            keys = list(string.Formatter().parse(template))
            if do_extrapolate or keys[-1][1] == 'ext':        # FIXME: "ext" is hard coded
                count = len(keys)-1
                current = sid.count('/')
                needed = count-current+1
                test = sid.replace('/**', '/*' * needed)
                if test in tested:
                    debug('Already tested, continue')
                    continue
                else:
                    tested.append(test)
                debug('Filled {}x* --> {}'.format(needed, test))
                matching = sid_to_dicts(test)
                debug('Got {}'.format(matching))
                for __type, data in six.iteritems(matching):
                    debug('found :' + __type)
                    found.append(__type)
                    if data and (do_extrapolate or (list(data)[-1] == 'ext')):  #
                        if uri:
                            new_sid = Sid('{}:{}?{}'.format(__type, test, uri))
                        else:
                            new_sid = Sid(__type + ':' + test)
                        debug('appending: {}'.format(new_sid.full_string))
                        result.append(new_sid)
            else:
                debug('Type "{}" is not a leaf, and do_extrapolate is False, skipped.')
                continue

    """
    #SMELL still sometimes we have the same result twice. Algo CBB.
    if len(result) != len(list(set(result))):
        print('Check expand...')
        print(len(result))
        print(len(list(set(result))))
        print(result)
        print(list(set(result)))
    """
    return list(set(result))


if __name__ == '__main__':

    from pprint import pprint
    from spil.util.log import setLevel, info, INFO, debug, DEBUG

    info('Tests start')

    setLevel(INFO)

    expandables = ['FTOT/S/*/**/ma', 'FTOT/A/**/V002/*/ma', 'FTOT', 'FTOT/A/**',
                   'FTOT/S/SQ0010/SH0010/ANI/**/abc',
                   'FTOT/S/**/mov',
                   'FTOT/S/SQ0010/SH0010/**/ma']

    expandables_with_uri = ['FTOT/S/*/**/ma?version=2', 'FTOT/S/*/**/ma?version=V002', 'FTOT/A/**/V002/*/ma?whatever', 'FTOT', 'FTOT/A/**',
                   'FTOT/S/SQ0010/SH0010/ANI/**/abc',
                   'FTOT/S/**/mov',
                   'FTOT/S/SQ0010/SH0010/**/ma?yes?yes']

    expandables_with_uri = ['FTOT/S/SQ0001/SH0020/**']

    # expandables_with_uri = ['FTOT/S/SQ0001/SH0020/**?state=WIP&version=>']

    for sid in expandables_with_uri:
        print(sid + ' -->')
        results = expand(sid, do_extrapolate=False)
        # print('Expanded to -->' + str(results))
        for result in results:
            print(result.type)
            print(result.string)
            # print(sid_to_dict(result, result.type))

        pprint(results)

        print('*'*10)
