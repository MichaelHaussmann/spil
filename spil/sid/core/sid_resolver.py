# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from __future__ import annotations
from typing import Tuple, List

"""
Sid resolver
Transforms the sid string into a valid sid dict, and reverse.
"""
import string
from collections import OrderedDict

import spil.vendor  # SMELL
import lucidity
from lucidity import Template

from spil.util.caching import lru_kw_cache as cache
from spil.util.log import debug, info
from spil.util.exception import SpilException

# sid conf
from spil.conf import key_types, sidtype_keytype_sep
from spil.conf import sip, sid_templates  # , meta_items # sid_filters


@cache
def sid_to_dict(sid: str, _type: str | None = None) -> Tuple[str, dict] | Tuple[None, None]:
    """
    Parses a given "sid" string using the existing sid_config templates.
    If "_type" is given, only the template named after the given "_type" is parsed.

    Returns a tuple with the type and the parsed data in an OrderedDict.
    If the parsing failed (no template matching) returns a None, None tuple.

    This function parses all templates in one go, so data from the first matching template is returned.
    This is the normal usage (as opposed to sid_to_dicts)

    :param sid:
    :param _type:
    :return:
    """

    if _type:
        template = Template(_type, sid_templates.get(_type),
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',
                            duplicate_placeholder_mode=lucidity.Template.STRICT)

        templates = [template]

    else:
        templates = []
        for name, pattern in sid_templates.items():
            template = Template(name, pattern,
                                anchor=lucidity.Template.ANCHOR_BOTH,
                                default_placeholder_expression='[^/]*',
                                duplicate_placeholder_mode=lucidity.Template.STRICT)

            templates.append(template)

    try:
        data, template = lucidity.parse(str(sid), templates)
        # print 'found', data, template
    except lucidity.ParseError as e:
        debug('Lucidity did not find a matching pattern. Type given: {} (Message: "{}")'.format(_type, e))
        return None, None

    if not data:
        return None, None

    # Sorting the result data into an OrderedDict()
    sid_type = template.name.split(sidtype_keytype_sep)[0]
    keys = key_types.get(sid_type)  # using template to get sorted keys
    keys = filter(lambda x: x in template.keys(), keys)  # template.keys() is a set

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    return template.name, ordered

@cache
def sid_to_dicts(sid: str) -> dict:
    """
    Parses a given "sid" using the existing sid_config templates.
    Returns a dict with the types and the parsed data.

    This function parses all templates separately, so data from all matching templates are returned.
    This usage is not standard (as opposed to sid_to_dict).
    It makes sense only for broad read sids (including /**) where we want to catch-all types.

    :param sid:
    :return:
    """
    results = {}  # OrderedDict() TODO: check behaviour py2 != py3

    # instantiating lucidity Templates
    for name, pattern in sid_templates.items():
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                            duplicate_placeholder_mode=lucidity.Template.STRICT)

        # try template parse
        try:
            data, template = lucidity.parse(str(sid), [template])
        except lucidity.ParseError as e:
            # ParseErrors are normal, we force the parsing of all the templates, and not just the first that matches, as usually
            continue

        if not data:
            continue

        # Sorting the result data into an OrderedDict()
        sid_type = template.name.split(sidtype_keytype_sep)[0]
        keys = key_types.get(sid_type)  # using template to get sorted keys
        keys = filter(lambda x: x in template.keys(), keys)  # template.keys() is a set

        data = data.copy()
        ordered = OrderedDict()
        for key in keys:
            ordered[key] = data.get(key)

        results[template.name] = ordered

    return results


def dict_to_sid(data: dict, _type: str | None = None) -> str:
    """
    Formats the given "data" dictionary using the given template "_type".
    If "_type" is not given it is detected using "dict_to_type".

    Returns the sid string.

    :param data:
    :param _type:
    :return:
    """
    if not data:
        raise SpilException('[dict_to_sid] Data is empty')

    data = data.copy()

    if not _type:
        _type = dict_to_type(data)

    pattern = sid_templates.get(_type)

    if not pattern:
        raise SpilException(
            '[dict_to_sid] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(_type, data))

    template = lucidity.Template(_type, pattern)

    if not template:
        raise SpilException('toe')
    try:
        sid = template.format(data).rstrip(sip)
    except lucidity.error.FormatError as e:
        debug('Lucidity could not format the Sid. Data: {} / type: {} (Message: "{}")'.format(data, _type, e))
        return ''  # TODO: test this

    return sid


def dict_to_type(data: dict, all: bool = False) -> str | List[str]:  # SMELL - this code is obscure and should be replaced / not be used
    """
    Retrieves the sid_keytypes for the given dict "data".
    "data" can be unsorted.

    If "all" is False (default), the first matching type is returned.
    If "all" is set to True, of list of corresponding types is returned,
    although usually a single type should match.

    The types are found by:
    - comparing the keys of the dict with the keys of the existing templates
    - in case of matching keys, applying the template and resolving it back to a dict

    Multiple matching types is a sign for a configuration problem.
    It is logged using debug('Sid multitypes for  =>')

    :param data:
    :param all:
    :return:
    """

    found = []

    keys = data.keys()

    for _type, template in sid_templates.copy().items():  # SMELL: this whole code is obscure...

        template_keys = [t[1] for t in string.Formatter().parse(template) if t[1] is not None]

        if len(keys) == len(template_keys):
            if set(keys) == set(template_keys):
                ltemplate = lucidity.Template(_type, template)
                test = ltemplate.format(data)
                if test:
                    debug('Checking matching types ... (fails are normal)')  #FIXME / #SMELL : this code is plain nonsense...
                    a, b = sid_to_dict(test, _type)
                    if a:
                        # print _type
                        found.append(_type)

    if not found:
        info('No type found for {}'.format(data))
        return ''

    if len(found) > 1:
        debug('Sid multitypes for  => {} // {}'.format(data, found))

    if all:
        return found
    else:
        return found[0]


if __name__ == '__main__':

    from spil.util.log import setLevel, INFO, info, warning
    from scripts.example_sids import sids

    info('Tests start')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    tests = ['hamlet/s/*']

    for test in tests:

        info('*' * 15)
        info('Testing : {}'.format(test))

        __, _dict = sid_to_dict(test)
        info('sid {} ---> \n{}'.format(test, _dict))

        a_type = dict_to_type(_dict)
        info('type : {}'.format(a_type))

        info('------ keys : {}'.format(_dict.keys()))

        retour = dict_to_sid(_dict)
        info('retour: ' + retour)

        assert(test == retour)

        info('*' * 15)
        print('  ')

    info('*' * 30)
    info('*' * 30)
