# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
"""

Sid resolver

Is the low level under the Sid object.

Transforms the sid string into a valid sid dict, and reverse.

"""

# TODO : refacto into class
# TODO : use explicit project in resolve process, so we can have one configuration per project.
from collections import OrderedDict

import six

if six.PY3:
    import spil.vendor  # SMELL
import lucidity
from lucidity import Template
import string

from spil.vendor.py2_lru import lru_cache as cache

from spil.util.log import debug, info
from spil.util.exception import SpilException

# sid conf
from spil.conf import sip, key_types, sidtype_keytype_sep
from spil.conf import sid_templates  # , meta_items # sid_filters

@cache
def sid_to_dict(sid, _type=None):
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

    # instantiating lucidity Templates
    templates = []
    for name, pattern in six.iteritems(sid_templates):
        if _type and not _type == name:  # FIXME: if _type is given, we should not loop at all, or should we?
            continue
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        # template.template_resolver = resolvers
        templates.append(template)

    # try template parse
    try:
        data, template = lucidity.parse(str(sid), templates)
        #print 'found', data, template
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
def sid_to_dicts(sid):
    """
    Parses a given "sid" using the existing sid_config templates.
    Returns a dict with the types and the parsed data.

    This function parses all templates separately, so data from all matching templates are returned.
    This usage is not standard (as opposed to sid_to_dict).
    It makes sense only for broad search sids (including /**) where we want to catch-all types.

    :param sid:
    :return:
    """
    results = {}

    # instantiating lucidity Templates
    for name, pattern in six.iteritems(sid_templates):
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        # template.template_resolver = resolvers

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


def dict_to_sid(data, _type=None):
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


def dict_to_type(data, all=False):  # SMELL - this code is obscure and should be replaced / not be used
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

    for _type, template in six.iteritems(sid_templates.copy()):  # SMELL: this whole code is obscure...

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

    from spil.util.log import setLevel, INFO, info

    info('Tests start')

    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    tests = ['raj/s']  # TODO: import test Sids

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

        info('*'*15)
        print('  ')

    info('*' * 30)
    info('*' * 30)
