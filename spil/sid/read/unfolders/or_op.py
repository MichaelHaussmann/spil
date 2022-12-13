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
from spil.sid.core import uri_helper


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
    """
    >>> or_op('bla/s/bla/A,B/**/one,two?test=X,Y,Z')
    ['bla/s/bla/A/**/one?test=X', 'bla/s/bla/A/**/one?test=Y', 'bla/s/bla/A/**/one?test=Z', 'bla/s/bla/B/**/one?test=X', 'bla/s/bla/B/**/one?test=Y', 'bla/s/bla/B/**/one?test=Z', 'bla/s/bla/A/**/two?test=X', 'bla/s/bla/A/**/two?test=Y', 'bla/s/bla/A/**/two?test=Z', 'bla/s/bla/B/**/two?test=X', 'bla/s/bla/B/**/two?test=Y', 'bla/s/bla/B/**/two?test=Z']
    """

    sid = str(sid)
    if not sid.count(ors):  # no "or" operators in sid.
        return [sid]

    if sid.count('?'):  # sid contains URI ending. We put it aside, and later append it back
        sid, uri = sid.split('?', 1)
    else:
        uri = ''

    sids = or_on_path(sid)

    result = []
    if uri:
        uris = or_on_uri(uri)
        for s in sids:
            for u in uris:
                result.append('{}?{}'.format(s, u))
    else:
        result = sids

    return result


def or_on_path(sid):
    """

    >>> or_on_path('bla/s/bla/A,B,C/**/one,two,three')
    ['bla/s/bla/A/**/one', 'bla/s/bla/B/**/one', 'bla/s/bla/C/**/one', 'bla/s/bla/A/**/two', 'bla/s/bla/B/**/two', 'bla/s/bla/C/**/two', 'bla/s/bla/A/**/three', 'bla/s/bla/B/**/three', 'bla/s/bla/C/**/three']
    """

    _start = '--start--'

    parts = sid.split(sip)

    found = [_start]
    for part in parts:
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


def or_on_uri(uri):
    """
    Applies the or operator to values of the uri, creating unique uris without the operator.

    >>> or_on_uri('titi=tata,blip&roger=vadim,bom,tom, tata')
    ['titi=tata&roger=vadim', 'titi=blip&roger=vadim', 'titi=tata&roger=bom', 'titi=blip&roger=bom', 'titi=tata&roger=tom', 'titi=blip&roger=tom', 'titi=tata&roger=tata', 'titi=blip&roger=tata']
    """

    uri_dict = uri_helper.to_dict(uri)
    result = [uri_dict.copy()]
    for key, value in uri_dict.items():
        if value.count(ors):
            new_result = []
            for i in value.split(ors):
                for d in result[:]:
                    new_dict = d.copy()
                    new_dict[key] = i
                    new_result.append(new_dict)
            result = new_result
#     print(result)

    return [uri_helper.to_string(d) for d in result]


if __name__ == '__main__':

    import doctest
    doctest.testmod()

