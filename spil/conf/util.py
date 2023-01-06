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

from spil.conf import sidtype_keytype_sep


def get_keys(template):
    return [t[1] for t in string.Formatter().parse(template) if t[1] is not None]


def extrapolate_templates(sid_templates, key_types, to_extrapolate=[], leaf_subtype='file'):
    """
    Templates are extrapolated: leave type entries are looped downwards to create subtypes.

     # type asset
    >>> sid_templates = {'asset__file': '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}'}
    >>> extrapolate_types = {'asset': ['project', 'type', 'assettype', 'asset', 'task', 'version', 'state', 'ext']}
    >>> to_extrapolate = ['asset__file']
    >>> extrapolation_leaf_subtype = 'file'
    >>> extrapolate_templates(sid_templates, extrapolate_types, to_extrapolate, extrapolation_leaf_subtype)
    OrderedDict([('asset__file', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}'), ('asset__state', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}'), ('asset__version', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}'), ('asset__task', '{project}/{type:a}/{assettype}/{asset}/{task}'), ('asset__asset', '{project}/{type:a}/{assettype}/{asset}'), ('asset__assettype', '{project}/{type:a}/{assettype}'), ('asset__type', '{project}/{type:a}'), ('asset__project', '{project}')])

    >>> sid_templates = {'asset__version': '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{state}/{version}',}
    >>> extrapolate_types = {'asset': ['project', 'type', 'assettype', 'asset', 'step', 'task', 'state', 'version', 'ext'],}
    >>> to_extrapolate = ['asset__version']
    >>> extrapolation_leaf_subtype = 'version'
    >>> extrapolate_templates(sid_templates, extrapolate_types, to_extrapolate, extrapolation_leaf_subtype)
    OrderedDict([('asset__version', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{state}/{version}'), ('asset__state', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{state}'), ('asset__task', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}'), ('asset__step', '{project}/{type:a}/{assettype}/{asset}/{step}'), ('asset__asset', '{project}/{type:a}/{assettype}/{asset}'), ('asset__assettype', '{project}/{type:a}/{assettype}'), ('asset__type', '{project}/{type:a}'), ('asset__project', '{project}')])

    """

    generated = OrderedDict()
    skipped = OrderedDict()

    # first we copy all the full paths, they have to match first
    for sid_type, template in sid_templates.items():
        if sid_type.endswith(leaf_subtype):
            print("adding {sid_type} ?")
            generated[sid_type] = template

    # then we start over to generate the subtypes
    for sid_type, template in sid_templates.items():

        # adding the current found
        if sid_type not in generated.keys():
            print("adding {sid_type} ?")
            generated[sid_type] = template

        # if there is an explicit list of types to extrapolate we use only these
        if to_extrapolate and (sid_type not in to_extrapolate):
            print(f"skipping {sid_type}")
            continue

        # generating sub keys
        if sid_type.endswith(leaf_subtype):
            parts = template.split('/')
            #keys = get_keys(template)
            basetype = sid_type.split(sidtype_keytype_sep)[0]
            keys = key_types.get(basetype)
            print(f"Handling {basetype} / {keys}")

            for i, key in enumerate(reversed(keys[:-1]), 1):

                new_type = sid_type.replace(leaf_subtype, key)
                new_template = '/'.join(parts[:-1 * i])
                print(f"New Type: {key} / {new_type} -> {new_template}")
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
    Uses the key_patterns dict to replace parts of the template according to the type.

    Example:
    For this entry in sid_templates :
    ('asset__file',            '{project}/{type:a}/{cat}/{name}/{task}/{version}/{state}/{ext:scenes}'),

    And this entry in key_patterns:
    'asset__': {
        '{task}': r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
    },

    For all types containing "asset__*", the entry {task} is replaced by r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
    Meaning that the asset tasks are specified in the asset templates.

    :param sid_templates:
    :param key_patterns:
    :return:
    """

    for _keytype, template in sid_templates.copy().items():

        for m in key_patterns.keys():
            if m in _keytype:
                for find, replace in key_patterns.get(m).items():
                    template = template.replace(find, replace)

        sid_templates[_keytype] = template



if __name__ == '__main__':

    from pprint import pprint

    sid_templates = {'asset__version': '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{state}/{version}', }
    extrapolate_types = {
        'asset': ['project', 'type', 'assettype', 'asset', 'step', 'task', 'state', 'version', 'ext'], }
    to_extrapolate = ['asset__version']
    extrapolation_leaf_subtype = 'version'
    result = extrapolate_templates(sid_templates, extrapolate_types, to_extrapolate, extrapolation_leaf_subtype)

    pprint(result)

    import doctest
    #doctest.testmod()
    """
    log.debug('Starting')
    log.debug('Path Templates: ')
    for k, v in path_templates.items():
        log.info('{} -> {}'.format(k, v))

    log.debug('')
    log.debug('Tests:')
    test_fs_duplicates()
    test_missing()

    log.debug('Done')
    """
