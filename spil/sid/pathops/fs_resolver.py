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
from typing import Tuple

"""
File system resolver
Path <-> dict translation
"""
import os
from pathlib import Path
from collections import OrderedDict

import spil.vendor  # SMELL
import lucidity
from lucidity import Template

from spil.util.caching import lru_kw_cache as cache
from spil.util.log import debug
from spil.util.exception import SpilException

from spil.util import utils
from spil.conf import key_types, sidtype_keytype_sep
from spil.sid.core.sid_resolver import dict_to_type, sid_to_dict
from spil.sid.pathops.pathconfig import get_path_config, PathConfig


def get_resolvers(config: PathConfig) -> dict:
    """
    Technical necessity for Lucidity template reference mechanism.

    :param config:
    :return: dict
    """
    return {
        config.path_templates_reference: Template(
            config.path_templates_reference, config.path_templates.get(config.path_templates_reference)
        )
    }

@cache
def path_to_dict(path: str | os.PathLike[str],
                 _type: str | None = None,
                 config: str = None) -> Tuple[str, dict] | Tuple[None, None]:
    """
    Resolves the given path into the matching data dictionary.
    Uses the _type, if given, else looks up all templates and uses the first matching one.

    Uses the Lucidity template mechanism,
    then applies configured mappings.

    Returns a tuple with the type and the parsed data in an OrderedDict.
    If the parsing failed (no template matching) returns a None, None tuple.

    """
    pc = get_path_config(config)
    resolvers = get_resolvers(pc)

    path = str(path)
    path = path.replace(os.sep, '/')

    if _type:
        template = Template(_type, pc.path_templates.get(_type),
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        template.template_resolver = resolvers
        templates = [template]

    else:
        templates = []
        for name, pattern in pc.path_templates.items():
            template = Template(name, pattern,
                                anchor=lucidity.Template.ANCHOR_BOTH,
                                default_placeholder_expression='[^/]*',
                                duplicate_placeholder_mode=lucidity.Template.STRICT)
            template.template_resolver = resolvers
            templates.append(template)

    try:
        data, template = lucidity.parse(path, templates)
        # print 'found', data, template
    except lucidity.ParseError as e:
        debug('Lucidity did not find a matching pattern. Type given: {} (Message: "{}")'.format(_type, e))
        return None, None

    if not data:
        return None, None

    # path mapping
    for key, value in data.items():
        # debug('{}, {}, {}'.format(key, value, template.name))
        if pc.path_mapping.get(key):
            value = pc.path_mapping.get(key).get(value, value)
            data[key] = value

            mapping = pc.path_mapping.get((key, template.name))  # type specific mapping
            if mapping:
                data[key] = mapping.get(value, value)

    # mapping from extra keys
    for new_key, sid_mapping in pc.extrakeys_to_sidkeys.items():
        if new_key in data:
            for key, _dict in sid_mapping.items():
                map_result = _dict.get(data.get(new_key))
                if map_result:
                    data[key] = map_result

    # Sorting the result data into an OrderedDict()
    sid_type = template.name.split(sidtype_keytype_sep)[0]
    keys = key_types.get(sid_type)  # using template to get sorted keys
    keys = filter(lambda x: x in data.keys(), keys)  # template.keys() is a set #

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    return template.name, ordered


def dict_to_path(data: dict, _type: str | None = None, config: str | None = None) -> os.PathLike[str]:
    """
    Resolves the given data dictionary into a path.
    Uses the _type, if given, else calls dict_to_type to find matching type.

    Uses the Lucidity template mechanism.
    Applies configured mappings and defaults before template formatting.

    Returns path string.
    """
    if not data:
        raise SpilException('[dict_to_path] Data is empty')

    pc = get_path_config(config)
    resolvers = get_resolvers(pc)

    data = data.copy()

    debug('Data: {}'.format(data))

    # setting defaults on empty values
    for key in data.keys():
        if not data.get(key) and pc.path_defaults.get(key):
            data[key] = pc.path_defaults.get(key)

    if not _type:
        _type = dict_to_type(data)

    # reverse path mapping
    for key, value in data.items():
        if value and pc.path_mapping.get(key):
            mapping = pc.path_mapping.get(key)  # global mapping
            data[key] = utils.get_key(mapping, value, value)

            mapping = pc.path_mapping.get((key, _type))  # type specific mapping
            if mapping:
                data[key] = utils.get_key(mapping, value, value)

    debug('sidtype: {}'.format(_type))

    pattern = pc.path_templates.get(_type)

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
        if key not in data.keys() and pc.path_defaults.get(key):
            data[key] = pc.path_defaults.get(key)

    # adding extra keys
    for key in pc.sidkeys_to_extrakeys.keys():
        if key in data.keys():
            for new_key, mapping in pc.sidkeys_to_extrakeys.get(key, {}).items():
                data[new_key] = mapping.get(data.get(key))

    debug('data after path_defaults: {}'.format(data))
    path = template.format(data)

    debug('found: {}'.format(path))

    return Path(path)


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

        _type, _dict = sid_to_dict(test)
        info('Dict ({}) ---> \n{}'.format(_type, _dict))

        try:
            path = dict_to_path(_dict, _type=_type, config='server')
            info(f'Path: {path}')

            __, retour = path_to_dict(path, config='server')
            info('Retour ({}) ---> \n{}'.format(_type, retour))

            assert (_dict == retour)

        except SpilException as se:
            warning(se)

        info('*' * 15)
        print('  ')

    info('*' * 30)
    info('*' * 30)
