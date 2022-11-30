# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
URI style string handling helper functions.

TODO: Sid URI handling needs to be streamlined and documented.
"""
from urllib.parse import urlencode
from urllib import parse as urlparse

from spil.sid.core import sid_resolver
from spil import conf
from spil.util.log import warning, debug
from spil.util.exception import SpilException


def to_dict(uri_string):
    """
    Converts a uri string into a dictionary.

    All ? can be used as &.
    Optionally leading or rtailing ? or & are ignored.

    Examples:
    >>> to_dict('keyA=valueA&keyB=valueB, XX')
    {'keyA': 'valueA', 'keyB': 'valueB, XX'}

    >>> to_dict('?keyA=valueA&keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    >>> to_dict('?keyA=valueA?keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    """
    uri_string = uri_string.replace('?', '&')  # we allow a=b?x=y but change it to a proper uri: a=b&x=y

    # cleaning start / end signs
    if uri_string.startswith('&'):
        uri_string = str(uri_string[1:])

    if uri_string.endswith('&'):
        uri_string = str(uri_string[:-1])

    uri_pairs = dict(urlparse.parse_qsl(urlparse.urlsplit('?' + uri_string).query))
    return uri_pairs


def to_string(uri_dict):
    """
    Converts a uri dict into a string.
    Does not do urlencoding, just strips whitespaces.

    Examples:
    >>> to_string({'keyA': 'valueA', 'keyB': 'valueB, BB'})
    'keyA=valueA&keyB=valueB,BB'
    """
    def encode(x, *args, **kwargs):
        return x.replace(' ', '')

    return urlencode(uri_dict, quote_via=encode)


def update(data, uri, option_prefix='~'):
    """
    Updates given dict with given uri into a new dict.

    If the URI value starts with option_prefix, it is only updated (if the key exists), not added.

    Option_prefix are removed from values, unless set to None.
    Keys and values are supposed to be strings.

    Examples:
    >>> update({'keyA': 'valueA', 'keyB': 'valueB'}, 'keyB=~replaceB&keyC=~skip this&keyD=keep this')
    {'keyA': 'valueA', 'keyB': 'replaceB', 'keyD': 'keep this'}

    >>> update({'keyA': 'valueA'}, 'keyB=~valueB', option_prefix=None)
    {'keyA': 'valueA', 'keyB': '~valueB'}

    >>> update({'keyA': 'valueA'}, 'keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}
    """
    data = data.copy()
    new_data = to_dict(uri)

    for key, value in new_data.items():

        if option_prefix:
            if str(value).startswith(str(option_prefix)):
                value = str(value).replace(option_prefix, '')
                is_value_optional = True
            else:
                is_value_optional = False
        else:
            is_value_optional = False

        if key in data.keys() or (not is_value_optional):
            data[key] = value

    return data


def apply_uri(string, uri=None, type=None, data=None):
    """
    Uri integration algorithm:
    - the URI key/values are applied to the existing data dict --> uri_helper.update
    - the data dictionary is submitted to type resolve --> sid_resolver.dict_to_type(data, all=True)
    - if a single type is resolved, it is now used, integration done.
    - else if no type is resolved, the URI is not applied (kept in the string, the data and type are unchanged)
    - else if multiple types are resolved, the URI is not applied (kept in the string, the previous data and type are unchanged)

    This is a problem in case of a search Sid, which could be poly-typed.

    Examples.

    Uri updates the sequence:
    >>> apply_uri('hamlet/s/sq01', uri='sequence=sq03', type='shot__sequence', data={'project':'hamlet','type':'s','sequence':'sq01'})
    ('hamlet/s/sq03', 'shot__sequence', {'project': 'hamlet', 'type': 's', 'sequence': 'sq03'})

    Uri adds a shot:
    >>> apply_uri('hamlet/s/sq01', uri='shot=sh010', type='shot__sequence', data={'project':'hamlet','type':'s','sequence':'sq01'})
    ('hamlet/s/sq01/sh010', 'shot__shot', {'project': 'hamlet', 'type': 's', 'sequence': 'sq01', 'shot': 'sh010'})

    Uri updates the sequence and adds a shot:
    >>> apply_uri('hamlet/s/sq01', uri='sequence=*&shot=sh010', type='shot__sequence', data={'project':'hamlet','type':'s','sequence':'sq01'})
    ('hamlet/s/*/sh010', 'shot__shot', {'project': 'hamlet', 'type': 's', 'sequence': '*', 'shot': 'sh010'})

    Uri contains undigestable data (wrong sequence format), and is not applied:
    >>> apply_uri('hamlet/s/sq01', uri='sequence=fuzz', type='shot__sequence', data={'project':'hamlet','type':'s','sequence':'sq01'})
    ('hamlet/s/sq01?sequence=fuzz', 'shot__sequence', {'project': 'hamlet', 'type': 's', 'sequence': 'sq01'})
    """
    if not type and data:
        raise SpilException("Uri can only be applied on typed data.")

    if not uri:
        return string, type, data

    _type = type

    new_data = update(data, uri)
    new_types = sid_resolver.dict_to_type(new_data, all=True)

    if not new_types:
        warning(f'[Sid] After URI apply, Sid "{string}" has no type. URI will not be applied.')
        string = '{}?{}'.format(string, uri)
        return string, _type, data

    if len(new_types) > 1:
        if _type not in new_types:
            if any(s in '{}?{}'.format(string, uri) for s in conf.search_symbols):
                debug(f'[Sid] After URI apply, Sid "{string}" matches different types: {new_types}. '
                      f'But it is a Search, so URI will be applied.')
                # URI will be applied, using the first new_types (# FIXME: refuse the temptation to guess)
            else:
                warning(f'[Sid] After URI apply, Sid "{string}" matches different types: {new_types}. '
                        f'URI will not be applied.')
                string = '{}?{}'.format(string, uri)
                return string, _type, data

    # data updated by URI is OK
    new_string = sid_resolver.dict_to_sid(new_data, new_types[0])
    if new_string:
        return new_string, new_types[0], new_data
    else:
        raise SpilException(f"Sid: [{string}?{uri}] : Uri was correctly applied, but unable to resolve back to Sid")


if __name__ == '__main__':
    """
    Test block.
    Launches doc test (test in the doc).
    
    In PY2 the test does not pass, because the dict is not sorted by default.
    """
    from spil.util.log import info, setLevel, INFO

    setLevel(INFO)

    info('Tests start')

    import doctest
    # info(doctest)

    doctest.testmod()

    r = to_dict('&keyA=valueA&keyB=valueB&')
    # print(r)

    info('Tests done.')
