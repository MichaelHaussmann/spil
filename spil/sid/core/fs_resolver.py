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

File system resolver

Path <-> dict translation

"""
from collections import OrderedDict

import six
import os

from spil.sid.core.sid_resolver import dict_to_type, sid_to_dict

if six.PY3:
    import spil.vendor  # forces import of patched lucidity
import lucidity
from lucidity import Template

from spil.util import utils
from spil.util.exception import SpilException
from spil.util.log import debug, warn, info

from spil import conf
from spil.conf import path_templates, path_templates_reference, path_mapping, path_defaults
from spil.conf import sidtype_keytype_sep, key_types

resolvers = {path_templates_reference: Template(path_templates_reference, path_templates.get(path_templates_reference))}


def path_to_dict(path, _type=None):

    path = str(path)
    # path = os.path.normcase(path)
    path = path.replace(os.sep, '/')

    templates = []
    for name, pattern in six.iteritems(path_templates):
        if _type and not _type == name:  # FIXME: if _type is given, we should not loop at all, or should we?
            continue
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # needed to use '#' for a path
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        template.template_resolver = resolvers

        templates.append(template)

    try:
        data, template = lucidity.parse(path, templates)
        # print 'found', data, template
    except Exception as e:
        warn(e)
        return None, None

    if not data:
        return None, None

    # path mapping
    for key, value in six.iteritems(data):
        if path_mapping.get(key):
            value = path_mapping.get(key).get(value, value)
            data[key] = value

    # mapping from extra keys
    for new_key, sid_mapping in six.iteritems(conf.extrakeys_to_sidkeys):
        if new_key in data:
            for key, _dict in six.iteritems(sid_mapping):
                data[key] = _dict.get(data.get(new_key))

    # Sorting the result data into an OrderedDict()
    sid_type = template.name.split(sidtype_keytype_sep)[0]
    keys = key_types.get(sid_type)  # using template to get sorted keys
    keys = filter(lambda x: x in data.keys(), keys)  # template.keys() is a set #

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    return template.name, ordered


def dict_to_path(data, _type=None):

    if not data:
        raise SpilException('[dict_to_path] Data is empty')

    data = data.copy()

    debug('Data: {}'.format(data))

    # setting defaults on empty values
    for key in data.keys():
        if not data.get(key) and path_defaults.get(key):
            data[key] = path_defaults.get(key)

    if not _type:
        _type = dict_to_type(data)

    # reverse path mapping
    for key, value in six.iteritems(data):
        if value and path_mapping.get(key):
            mapping = path_mapping.get(key)
            data[key] = utils.get_key(mapping, value)

    debug('sidtype: {}'.format(_type))

    pattern = path_templates.get(_type)

    debug('pattern: {}'.format(pattern))

    if not pattern:
        raise SpilException('[dict_to_path] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(_type, data))

    template = Template(_type, pattern)
    template.template_resolver = resolvers

    debug('template: {}'.format(template))

    if not template:
        raise SpilException('toe')

    # adding template specific defaults
    for key in template.keys():
        if key not in data.keys() and path_defaults.get(key):
            data[key] = path_defaults.get(key)

    # adding extra keys
    for key in conf.sidkeys_to_extrakeys.keys():
        if key in data.keys():
            for new_key, mapping in six.iteritems(conf.sidkeys_to_extrakeys.get(key, {})):
                data[new_key] = mapping.get(data.get(key))

    debug('data after path_defaults: {}'.format(data))
    path = template.format(data)

    debug('found: {}'.format(path))

    return path


if __name__ == '__main__':

    from spil.util.log import setLevel, INFO, info

    info('Tests start')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    # from spil.conf import test_sids as tests
    # from spil.tests.generate_test_sids import sids
    sids = []

    tests = ['demo/s/*']

    tests = (tests + sids)[:50]
    for test in tests:
        info('*' * 15)
        info('Testing : {}'.format(test))

        _type, _dict = sid_to_dict(test)
        info('Dict ({}) ---> \n{}'.format(_type, _dict))

        try:
            path = dict_to_path(_dict, _type=_type)
            info('Path: ' + path)

            __, retour = path_to_dict(path)
            info('Retour ({}) ---> \n{}'.format(_type, retour))

            assert (_dict == retour)

        except SpilException as se:
            warn(se)

        info('*' * 15)
        print('  ')

    info('*' * 30)
    info('*' * 30)
