"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Tuple, Optional

import os
from pathlib import Path
from collections import OrderedDict  # TODO: replace by dict

from resolva import Resolver

from spil.util.caching import lru_kw_cache as cache
from spil.util.log import debug
from spil.util.exception import SpilException
from spil.util import exception

from spil.util import utils
from spil.conf import key_types, sidtype_keytype_sep
from spil.sid.core.sid_resolver import dict_to_type, sid_to_dict
from spil.sid.pathops.pathconfig import get_path_config, PathConfig

"""
File system resolver
Path <-> dict translation
"""


@cache
def path_to_dict(
    path: str | os.PathLike[str], _type: Optional[str] = None, config: Optional[str] = None
) -> Tuple[str, dict] | Tuple[None, None]:
    """
    Resolves the given path into the matching data dictionary.
    Uses the _type, if given, else looks up all templates and uses the first matching one.

    Uses the Resolva template mechanism,
    then applies configured mappings.

    Returns a tuple with the type and the parsed data in an OrderedDict.
    If the parsing failed (no template matching) returns a None, None tuple.

    """
    path = str(path)
    path = path.replace(os.sep, "/")

    pc = get_path_config(config)
    r = Resolver.get(pc.name)

    if _type:
        data = r.resolve_one(path, _type)
        template = _type
    else:
        template, data = r.resolve_first(path)

    if not data:
        return None, None

    # path mapping
    for key, value in data.items():
        # debug('{}, {}, {}'.format(key, value, template.name))
        if pc.path_mapping.get(key):
            value = pc.path_mapping.get(key).get(value, value)
            data[key] = value

            mapping = pc.path_mapping.get((key, template))  # type specific mapping
            if mapping:
                data[key] = mapping.get(value, value)

    # mapping from extra keys
    for new_key, sid_mapping in pc.extrakeys_to_sidkeys.items():
        if new_key in data:
            for key, _dict in sid_mapping.items():
                map_result = _dict.get(data.get(new_key))
                if map_result:
                    data[key] = map_result

    # FIXME: remove extra sorting and Ordered dict ?
    # Sorting the result data into an OrderedDict()
    sid_type = template.split(sidtype_keytype_sep)[0]
    keys = key_types.get(sid_type)  # using template to get sorted keys
    keys = filter(lambda x: x in data.keys(), keys)  # template.keys() is a set #

    if data.keys() != r.get_keys_for(template):
        raise SpilException(f'Data was changed after resolve. Can this end well ? Initial keys: {r.get_keys_for(template)} / Data keys: {data.keys()} ')

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    return template, ordered


def dict_to_path(data: dict, _type: Optional[str] = None, config: Optional[str] = None) -> Path:
    """
    Resolves the given data dictionary into a path.
    Uses the _type, if given, else calls dict_to_type to find matching type.

    Uses the Resolva template mechanism.
    Applies configured mappings and defaults before template formatting.

    Returns path string.
    """
    if not data:
        raise SpilException("[dict_to_path] Data is empty")

    pc = get_path_config(config)
    r = Resolver.get(pc.name)

    data = data.copy()

    debug(f"Data: {data}")

    # setting defaults on empty values (before detecting the type)
    for key in data.keys():
        if not data.get(key) and pc.path_defaults.get(key):
            data[key] = pc.path_defaults.get(key)

    # detecting the type if not given
    if not _type:
        _type, __ = r.format_first(data)
        if not _type:
            raise SpilException(f'Unable to detect type for Data: "{data}"')

    # get template keys, which also checks if there is a matching pattern
    template_keys = (r.get_keys_for(_type)
                     or exception.raiser(f'Unable to find pattern for type: "{_type}" \nData: "{data}"'))

    # reverse path mapping
    for key, value in data.items():
        if value and pc.path_mapping.get(key):
            mapping = pc.path_mapping.get(key)  # global mapping
            data[key] = utils.get_key(mapping, value, value)

            mapping = pc.path_mapping.get((key, _type))  # type specific mapping
            if mapping:
                data[key] = utils.get_key(mapping, value, value)

    # adding template specific defaults
    for key in template_keys:
        if key not in data.keys() and pc.path_defaults.get(key):
            data[key] = pc.path_defaults.get(key)

    # adding extra keys
    for key in pc.sidkeys_to_extrakeys.keys():
        if key in data.keys():
            for new_key, mapping in pc.sidkeys_to_extrakeys.get(key, {}).items():
                data[new_key] = mapping.get(data.get(key))

    # Data is updated, formatting now
    debug(f"data after path_defaults: {data}")
    # path = r.format_one(data, _type) or exception.raiser(f'Unable to format Data: "{data}" with type: "{_type}" \n')

    if data.keys() != r.get_keys_for(_type):
        raise SpilException(f' ? Initial keys: {r.get_keys_for(_type)} / Dict keys: {data.keys()} ')

    # formatting without check  # FIXME: choose one method
    path = r.get_format_for(_type).format(**data)
    path_checked = r.format_one(data, _type)  # check at least if not None

    if path != path_checked:
        raise SpilException(f' ? Path returned after format is not matching checkless formatted. "{path}" v> {path_checked}')

    debug(f"found: {path}")

    return Path(path)


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO, info, warning

    info("Tests start")

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    tests = ["hamlet/s/*"]

    for test in tests:

        info("*" * 15)
        info("Testing : {}".format(test))

        _type, _dict = sid_to_dict(test)
        info("Dict ({}) ---> \n{}".format(_type, _dict))

        try:
            path = dict_to_path(_dict, _type=_type, config="server")
            info(f"Path: {path}")

            __, retour = path_to_dict(path, config="server")
            info("Retour ({}) ---> \n{}".format(_type, retour))

            assert _dict == retour

        except SpilException as se:
            warning(se)

        info("*" * 15)
        print("  ")

    info("*" * 30)
    info("*" * 30)
