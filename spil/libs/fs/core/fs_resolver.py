# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


File system resolver

Path <-> dict translation

"""
import six
if six.PY3:
    import spil.vendor
import lucidity
from lucidity import Template

from spil.libs.util import utils
from spil.libs.util.exception import SpilException
from spil.libs.util.log import debug, warn, info

from spil.conf.fs_conf import path_templates, path_templates_reference, path_mapping, path_defaults
from spil.conf.sid_conf import asset_keys, shot_keys, get_sidtype

resolvers = {path_templates_reference: Template(path_templates_reference, path_templates.get(path_templates_reference))}


def path_to_dict(path):

    path = str(path)

    templates = []
    for name, pattern in six.iteritems(path_templates):
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

    for key, value in six.iteritems(data):
        if path_mapping.get(key):
            value = path_mapping.get(key).get(value, value)
            data[key] = value

    for key in list(data.keys()):
        if key not in shot_keys + asset_keys:
            data.pop(key)

    return template.name, data  # need the name ?


def dict_to_path(data):

    if not data:
        raise SpilException('[dict_to_path] Data is empty')

    data = data.copy()

    debug('Data: {}'.format(data))

    # setting defaults
    for key in data.keys():
        if not data.get(key) and path_defaults.get(key):
            data[key] = path_defaults.get(key)

    # adding defaults

    # reverse path mapping
    for key, value in six.iteritems(data):
        if value and path_mapping.get(key):
            mapping = path_mapping.get(key)
            data[key] = utils.get_key(mapping, value)

    subtype = get_sidtype(data)

    debug('sidtype: {}'.format(subtype))

    pattern = path_templates.get(subtype)

    debug('pattern: {}'.format(pattern))

    if not pattern:
        raise SpilException('[dict_to_path] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(subtype, data))

    template = Template(subtype, pattern)
    template.template_resolver = resolvers

    debug('template: {}'.format(template))

    if not template:
        raise SpilException('toe')

    # adding template specific defaults
    for key in template.keys():
        if key not in data.keys() and path_defaults.get(key):
            data[key] = path_defaults.get(key)

    debug('data after path_defaults: {}'.format(data))
    path = template.format(data)

    debug('found: {}'.format(path))

    return path


if __name__ == '__main__':

    print('Tests are in spil.tests')