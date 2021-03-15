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
from collections import OrderedDict
import six

from spil.conf import sidtype_keytype_sep


def get_keys(template):
    return [t[1] for t in string.Formatter().parse(template) if t[1] is not None]


def extrapolate(sid_templates, key_types):
    """
    Templates are extrapolated: leave type entries are looped downwards to create subtypes.

    """

    generated = OrderedDict()
    skipped = OrderedDict()

    # first we copy all the full paths, they have to match first
    for keytype, template in six.iteritems(sid_templates):
        if keytype.endswith('file'):  # FIXME: hard coded !
            generated[keytype] = template

    # then we start over to generate the subtypes
    for keytype, template in six.iteritems(sid_templates):

        # adding the current found
        if keytype not in generated.keys():
            generated[keytype] = template

        # generating sub keys
        if keytype.endswith('file'):
            parts = template.split('/')
            # keys = get_keys(template)
            # print(keytype.split(sidtype_keytype_sep)[0])
            keys = key_types.get(keytype.split(sidtype_keytype_sep)[0])
            # print(keys)
            for i, key in enumerate(reversed(keys[:-1]), 1):
                new_type = keytype.replace('file', key)
                new_template = '/'.join(parts[:-1 * i])

                # new_template = template.split('/{' + key)[0]  # for paths

                # we skip if template is already defined by another type
                if new_template in set(sid_templates.values()).union(set(generated.values())):
                    skipped[new_type] = new_template
                    continue

                # we skip if this type was already defined
                if new_type in set(sid_templates.keys()).union(set(generated.keys())):
                    skipped[new_type] = new_template
                    continue

                generated[new_type] = new_template

    """
    print('Skipped Entries:')
    for k, v in six.iteritems(skipped):
        print('{}  -->  {}'.format(k, v))

    print('Generated Dict:')
    for k, v in six.iteritems(generated):
        print('{}  -->  {}'.format(k, v))
    """

    return generated


def pattern_replacing(sid_templates, key_patterns):
    """
    Loops trough the templates in sid_templates
    Uses the key_patterns dict to replace parts of the template according to the keytype.

    Example:
    For this entry in sid_templates :
    ('asset__file',            '{project}/{type:a}/{cat}/{name}/{task}/{version}/{state}/{ext:scenes}'),

    And this entry in key_patterns:
    'asset__': {
        '{task}': r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
    },

    For all keytypes containing "asset__*", the entry {task} is replaced by r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
    Meaning that the asset tasks are specified in the asset templates.

    :param sid_templates:
    :param key_patterns:
    :return:
    """

    for _keytype, template in six.iteritems(sid_templates.copy()):

        for m in key_patterns.keys():
            if m in _keytype:
                for find, replace in six.iteritems(key_patterns.get(m)):
                    template = template.replace(find, replace)

        sid_templates[_keytype] = template
