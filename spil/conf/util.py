# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Mapping, List, Dict

import string
from collections import OrderedDict

from spil.util.log import debug
from spil.conf import sidtype_keytype_sep


def get_keys(template):
    return [t[1] for t in string.Formatter().parse(template) if t[1] is not None]


def extrapolate_templates(sid_templates: Mapping[str, str], to_extrapolate: List[str]) -> Mapping[str, str]:
    """
    This function receives the "sid_templates" dictionary, operates "extrapolation", and returns a modified "sid_templates" dict.
    "Extrapolation" is done for each "type" (sid type) listed in "to_extrapolate".

    "Extrapolation" means generating intermediate types (and templates) from a deeper type / longer template,
    by replacing each types "keytype" by the templates last key.

    Illustration.

        Suppose we have:
        type: shot__version, template: project/s/sequence/shot/task/version

        Extrapolation will generate:
        type: shot__task, template: project/s/sequence/shot/task
        type: shot__shot, template: project/s/sequence/shot
        type: shot__sequence, template: project/s/sequence
        type: shot__type, template: project/s
        type: shot__project, template: project

    The templates are used by the resolver.
    The goal of this function is to generate some automatically, to simplify configuration.

    Notes:
        Order of templates is important. Extrapolation starts when a "to_extrapolate" type is encountered,
        and the extrapolated types are inserted after that.
        If a type already exists in config, the generated type is skipped (not updated by extrapolation).
        If a template already exists in the config, the generated type is skipped also.

    Examples:

        >>> sid_templates = {'asset__file': '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',\
            'asset': '{project}/{type:a}',\
            'project': '{project}'}
        >>> to_extrapolate = ['asset__file']
        >>> extrapolate_templates(sid_templates, to_extrapolate)
        OrderedDict([('asset__file', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}'), ('asset__state', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}'), ('asset__version', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}'), ('asset__task', '{project}/{type:a}/{assettype}/{asset}/{task}'), ('asset__asset', '{project}/{type:a}/{assettype}/{asset}'), ('asset__assettype', '{project}/{type:a}/{assettype}'), ('asset', '{project}/{type:a}'), ('project', '{project}')])

        >>> sid_templates = {'asset__file': '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',\
            'asset__state': '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{version}/{state}',\
            'asset': '{project}/{type:a}',\
            'project': '{project}'}
        >>> to_extrapolate = ['asset__state']
        >>> extrapolate_templates(sid_templates, to_extrapolate)
        OrderedDict([('asset__file', '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}'), ('asset__state', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{version}/{state}'), ('asset__version', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{version}'), ('asset__task', '{project}/{type:a}/{assettype}/{asset}/{step}/{task}'), ('asset__step', '{project}/{type:a}/{assettype}/{asset}/{step}'), ('asset__asset', '{project}/{type:a}/{assettype}/{asset}'), ('asset__assettype', '{project}/{type:a}/{assettype}'), ('asset', '{project}/{type:a}'), ('project', '{project}')])

    Args:
        sid_templates: A dictionary containing sid types (template names) as keys, and templates (path like strings) as values.
        to_extrapolate: List of sid types that should be extrapolated

    Returns:
        A new template dictionary containing sid_templates and the insterted extrapolated types.
    """
    new_templates = OrderedDict()

    debug("Starting template extrapolation.")

    # We loop over the existing template dictionary
    for sid_type, template in sid_templates.items():

        new_templates[sid_type] = template
        debug(f"Adding existing {sid_type} / {template}")

        # if the type is to_extrapolate
        if sid_type in to_extrapolate:
            debug(f"Extrapolating: {sid_type}")

            # getting ingredients from the sid_type and template
            keytype = sid_type.split(sidtype_keytype_sep)[-1]
            parts = template.split('/')[:-1]  # we remove the last element, that is already in the sid_type

            # walking up the parts
            for i, part in enumerate(reversed(parts)):

                # key from the template part, eg: "{type:a}" => "type"
                key = part.split(':')[0].replace('{', '').replace('}', '')

                # building the new type and template
                new_type = sid_type.replace(keytype, key)
                new_template = '/'.join(parts[:len(parts)-i])

                # we skip if template is already defined by another type
                if new_template in set(sid_templates.values()).union(set(new_templates.values())):
                    debug(f"Already defined template, skipped: {new_template}")
                    continue

                # we skip if this type was already defined
                if new_type in set(sid_templates.keys()).union(set(new_templates.keys())):
                    debug(f"Already defined type, skipped: {new_type}")
                    continue

                debug(f"Adding: {key} / {new_type} -> {new_template}")
                new_templates[new_type] = new_template

    debug("Extrapolation done.")
    return new_templates


def pattern_replacing(sid_templates: Dict[str, str], key_patterns: Dict[str, Dict[str, str]]) -> None:
    """
    Loops through the templates in sid_templates.
    Uses the key_patterns dict to replace parts of the template according to the type.

    Modifies the given template dictionary in place. Does not return anything.

    Illustration:

        For this entry in sid_templates :
            'asset__file':'{project}/{type:a}/{cat}/{name}/{task}/{version}/{state}/{ext:scenes}'

        And this entry in key_patterns:
            'asset__': {
                '{task}': r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
            },

        For all types containing "asset__*", the entry {task} is replaced by r'{task:(' + '|'.join(asset_tasks) + '|\*)}',
        Meaning that the asset tasks are specified in the asset templates.

    Args:
        sid_templates: A dictionary containing sid types (template names) as keys, and templates (path like strings) as values.
        key_patterns: A dictionary, where key string is a pattern to match against a sid type, and value a replace dict.

    """

    for _keytype, template in sid_templates.copy().items():

        for m in key_patterns.keys():
            if m in _keytype:
                for find, replace in key_patterns.get(m).items():  # type: ignore
                    template = template.replace(find, replace)

        sid_templates[_keytype] = template


if __name__ == '__main__':

    from pprint import pprint
    sid_templates = {'asset__file': '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',
                     'asset': '{project}/{type:a}',
                     'project': '{project}'}
    to_extrapolate = ['asset__file']
    result = extrapolate_templates(sid_templates, to_extrapolate)
    pprint(result)

    sid_templates = {'asset__version': '{project}/{type:a}/{assettype}/{asset}/{step}/{task}/{state}/{version}', }
    to_extrapolate = ['asset__version']
    result = extrapolate_templates(sid_templates, to_extrapolate)
    pprint(result)

    import doctest
    doctest.testmod()

