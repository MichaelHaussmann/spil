"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from urllib.parse import urlencode
from urllib import parse as urlparse

from spil.sid.core import sid_resolver
from spil import conf
from spil.util.log import warning, debug
from spil.util.exception import SpilException

"""
Query style string handling helper functions.

TODO: Sid Query handling needs to be cleaned up, typed and documented.
"""


def to_dict(query_string):
    """
    Converts a query string into a dictionary.

    All ? can be used as &.
    Optionally leading or trailing ? or & are ignored.

    Examples:
    >>> to_dict('keyA=valueA&keyB=valueB, XX')
    {'keyA': 'valueA', 'keyB': 'valueB, XX'}

    >>> to_dict('?keyA=valueA&keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    >>> to_dict('?keyA=valueA?keyB=valueB')
    {'keyA': 'valueA', 'keyB': 'valueB'}

    """
    # we allow a=b?x=y but change it to a proper query: a=b&x=y
    query_string = query_string.replace("?", "&")

    # cleaning start / end signs
    if query_string.startswith("&"):
        query_string = str(query_string[1:])

    if query_string.endswith("&"):
        query_string = str(query_string[:-1])

    query_pairs = dict(urlparse.parse_qsl(urlparse.urlsplit("?" + query_string).query))
    return query_pairs


def to_string(query_dict):
    """
    Converts a query dict into a string.
    Does not do urlencoding, just strips whitespaces.

    Examples:
    >>> to_string({'keyA': 'valueA', 'keyB': 'valueB, BB'})
    'keyA=valueA&keyB=valueB,BB'
    """

    def encode(x, *args, **kwargs):
        return x.replace(" ", "")

    return urlencode(query_dict, quote_via=encode)  # noqa


def update(data, query, option_prefix="~"):
    """
    Updates given dict with given query into a new dict.

    If the Query value starts with option_prefix, it is only updated, if the key exists, not added.

    Option_prefix are removed from values, unless explicitely set to None.
    Keys and values are supposed to be strings.

    Examples:

        >>> update({'keyA': 'valueA', 'keyB': 'valueB'}, 'keyB=~replaceB&keyC=~skip this&keyD=add this')
        {'keyA': 'valueA', 'keyB': 'replaceB', 'keyD': 'add this'}

        >>> update({'keyA': 'valueA'}, 'keyB=~valueB', option_prefix=None)
        {'keyA': 'valueA', 'keyB': '~valueB'}

        >>> update({'keyA': 'valueA'}, 'keyB=valueB')
        {'keyA': 'valueA', 'keyB': 'valueB'}

    Args:
        data: a key:value dictionary
        query: a query string
        option_prefix: A sign prepended to a value, to indicate it is optional. "~"  by default.

    Returns: updated disctionary

    """
    if not data:  # may be None
        data = {}

    data = data.copy()
    new_data = to_dict(query)

    for key, value in new_data.items():

        if option_prefix:
            if str(value).startswith(str(option_prefix)):
                value = str(value).replace(option_prefix, "")
                is_value_optional = True
            else:
                is_value_optional = False
        else:
            is_value_optional = False

        if key in data.keys() or (not is_value_optional):
            data[key] = value

    return data


def apply_query(string, query=None, type=None, fields=None):
    """
    "Query application" algorithm:
    - the Query key/values update the existing fields dict --> query_helper.update
    - the updated fields dictionary is sent to the resolver to be typed --> sid_resolver.dict_to_type(fields, all=True)
    - if a single type is resolved, it is now used, integration done.
    - else if no type is resolved, the Query is not applied (kept in the string, the fields and type are unchanged)
    - else if multiple types are resolved:
        * if the original type is amongs the new types, it is used, integration done.
        * else if the sid is a search, the first type is used, integration done (#FIXME: this behaviour should change)
        * else the Query is not applied (kept in the string, the previous fields and type are unchanged)

    This is a problem in case of a read Sid, which could be poly-typed.

    Examples.
    (Note that the examples depend on "spil_hamlet_conf" example configuration. Failure may be due to non matching config)

    Query updates the sequence:
    >>> apply_query('hamlet/s/sq010', query='sequence=sq030', type='shot__sequence', fields={'project':'hamlet','type':'s','sequence':'sq010'})
    ('hamlet/s/sq030', 'shot__sequence', {'project': 'hamlet', 'type': 's', 'sequence': 'sq030'})

    Query adds a shot:
    >>> apply_query('hamlet/s/sq010', query='shot=sh0010', type='shot__sequence', fields={'project':'hamlet','type':'s','sequence':'sq010'})
    ('hamlet/s/sq010/sh0010', 'shot__shot', {'project': 'hamlet', 'type': 's', 'sequence': 'sq010', 'shot': 'sh0010'})

    Query updates the sequence and adds a shot:
    >>> apply_query('hamlet/s/sq010', query='sequence=*&shot=sh0010', type='shot__sequence', fields={'project':'hamlet','type':'s','sequence':'sq010'})
    ('hamlet/s/*/sh0010', 'shot__shot', {'project': 'hamlet', 'type': 's', 'sequence': '*', 'shot': 'sh0010'})

    Query contains undigestable fields (wrong sequence format), and is not applied:
    >>> apply_query('hamlet/s/sq010', query='sequence=fuzz', type='shot__sequence', fields={'project':'hamlet','type':'s','sequence':'sq010'})
    ('hamlet/s/sq010?sequence=fuzz', 'shot__sequence', {'project': 'hamlet', 'type': 's', 'sequence': 'sq010'})

    Works with empty string, fields and type
    >>> apply_query('', query='project=hamlet', type=None, fields=None)
    ('hamlet', 'project', {'project': 'hamlet'})
    """
    if not type and fields:
        raise SpilException("Query can only be applied on typed fields (or empty fields).")

    if not query:
        return string, type, fields

    _type = type

    new_data = update(fields, query)
    new_types = sid_resolver.dict_to_type(new_data, all=True)

    if not new_types:
        warning(f'[Sid] After Query apply, Sid "{string}" has no type. Query will not be applied.')
        string = "{}?{}".format(string, query)
        return string, _type, fields

    # After Query apply, if there is one single new type, we use this new type
    if len(new_types) == 1:
        _type = new_types[0]

    # if the Sid now matches multiple types, we have to choose
    elif len(new_types) > 1:

        # if the given type matches one of the new types, we keep the given type
        if _type in new_types:
            pass

        # if the given type does not match any of the new types
        else:
            # if the Sid is a search, we use the first of the new types.
            # TODO: this is arbitrary and should be warned or better handled.
            if any(s in "{}?{}".format(string, query) for s in conf.search_symbols):
                debug(
                    f'[Sid] After Query apply, Sid "{string}" matches different types: {new_types}. '
                    f"But it is a Search, so Query will be applied."
                )
                # Query will be applied, using the first new_types (# FIXME: refuse the temptation to guess)
                # In this case we should check if all the types result in the same Sid string, and return it, untyped.
                _type = new_types[0]
            else:
                warning(
                    f'[Sid] After Query apply, Sid "{string}" matches different types: {new_types}. '
                    f"Query will not be applied."
                )
                string = "{}?{}".format(string, query)
                return string, _type, fields

    # fields updated by Query is OK
    new_string = sid_resolver.dict_to_sid(new_data, _type)
    if new_string:
        return new_string, _type, new_data
    else:
        raise SpilException(
            f"Sid: [{string}?{query}] Query was correctly applied, but unable to resolve back to Sid"
        )


if __name__ == "__main__":
    """
    Launches doctest (test in the doc).
    """
    from spil.util.log import info, setLevel, INFO

    setLevel(INFO)

    info("Tests start")

    import doctest

    # info(doctest)

    doctest.testmod()

    r = to_dict("&keyA=valueA&keyB=valueB&")
    # print(r)

    info("Tests done.")
