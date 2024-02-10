"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Tuple, List, Optional, Mapping

from collections import OrderedDict

from resolva import Resolver

from spil.util.caching import lru_kw_cache as cache
from spil.util.log import debug, info
from spil.util.exception import SpilException, raiser

# sid conf
from spil.conf import key_types, sidtype_keytype_sep  # type: ignore
from spil.conf import sip, sid_templates  # type: ignore

"""
Sid resolver
Transforms the sid string into a valid sid dict, and reverse.
"""


@cache
def sid_to_dict(sid: str, _type: Optional[str] = None) -> Tuple[str, dict] | Tuple[None, None]:
    """
    Parses a given "sid" string using the existing sid_config templates.
    If "_type" is given, only the template named after the given "_type" is parsed.

    Returns a tuple with the type and the resolved data dict.
    If the parsing failed (no template matching) returns a None, None tuple.

    This function parses all templates in one go, so data from the first matching template is returned.
    This is the normal usage (as opposed to sid_to_dicts)

    Args:
        sid: a Sid string
        _type: a Sid type name, which is the key to the template in spil_sid_conf.

    Returns: a tuple with the type and the resolved data dict.

    """
    r = Resolver.get("sid")

    if _type:
        data = r.resolve_one(sid, _type)
        template = _type
    else:
        template, data = r.resolve_first(sid)

    if not data:
        return None, None

    # FIXME: remove extra sorting and Ordered dict ?
    # Sorting the result data into an OrderedDict()
    sid_type = template.split(sidtype_keytype_sep)[0]
    keys = key_types.get(sid_type)  # using template to get sorted keys
    keys = filter(lambda x: x in r.get_keys_for(template), keys)  # r.get_keys(template) is a set  # FIXME: should this happen ???!!!

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    if ordered.keys() != r.get_keys_for(template):
        raise SpilException(f' ? Initial keys: {r.get_keys_for(template)} / Dict keys: {ordered.keys()} ')

    return template, ordered


@cache
def sid_to_dicts(sid: str) -> Mapping[str, dict]:
    """
    Parses a given "sid" using the existing spil_sid_config templates.
    Returns a dict with the types and the resolved data.

    This function parses all templates separately, so data from all matching templates are returned.
    This usage is not standard (as opposed to sid_to_dict).
    It makes sense only for broad read sids (including /**) where we want to catch-all types.

    Args:
        sid: a Sid string

    Returns: a dictionary containing types as keys and resolved data as values.

    """
    results = {}
    r = Resolver.get("sid")

    # FIXME: sorting is not needed ? (at least could be factorised in one function)
    # instantiating lucidity Templates
    for template, data in r.resolve_all(sid).items():

        # Sorting the result data into an OrderedDict():
        # getting the type
        sid_type = template.split(sidtype_keytype_sep)[0]
        # using template to get sorted keys for this basetype
        keys = key_types.get(sid_type)
        # filter out unused keys
        keys = filter(lambda x: x in r.get_keys_for(template), keys)  # FIXME: should this happen ???!!!
        # building an Ordered dict with keys in right order
        data = data.copy()
        ordered = OrderedDict()
        for key in keys:
            ordered[key] = data.get(key)
        # appending the ordered dict to the results list
        results[template] = ordered

    return results


def dict_to_sid(data: dict, _type: Optional[str] = None) -> str:
    """
    Formats the given "data" dictionary using the given template "_type".
    If "_type" is not given it is detected using "dict_to_type".

    Returns the sid string.

    Args:
        data: a data dictionary with Sid fields
        _type: a Sid type name, which is the key to the template in spil_sid_conf.

    Returns: a Sid string

    """
    if not data:
        raise SpilException("[dict_to_sid] Data is empty")

    # result = ""

    # data = data.copy()
    r = Resolver.get("sid")

    if _type:
        result = r.format_one(data, _type)
    else:
        name, result = r.format_first(data)

    return result


def dict_to_type(data: dict, all: bool = False) -> str | List[str]:
    """
    Retrieves the sid types for the given dict "data".
    "data" can be unsorted.

    If "all" is False (default), the first matching type is returned.
    If "all" is set to True, of list of corresponding types is returned,
    although usually a single type should match.

    The types are found by:
    - comparing the keys of the dict with the keys of the existing templates
    - in case of matching keys, applying the template and resolving it back to a dict

    Multiple matching types is a sign for a configuration problem.
    It is logged using debug('Sid multitypes for  =>')

    Args:
        data: a data dictionary with Sid fields
        all: if set to True, all matching types are returned, else the first matching type is returned (default)

    Returns: the type or types resolved from the given data dictionary.
    """

    r = Resolver.get("sid")
    found = list(r.format_all(data).keys())

    if not found:
        info("No type found for {}".format(data))
        return ""

    if len(found) > 1:
        debug("Sid multitypes for  => {} // {}".format(data, found))

    if all:
        return found
    else:
        return found[0]


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO, info, warning

    info("Tests start")

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    tests = ["hamlet/s/*"]

    for test in tests:

        info("*" * 15)
        info("Testing : {}".format(test))

        __, _dict = sid_to_dict(test)
        info("sid {} ---> \n{}".format(test, _dict))

        a_type = dict_to_type(_dict)
        info("type : {}".format(a_type))

        info("------ keys : {}".format(_dict.keys()))

        retour = dict_to_sid(_dict)
        info("retour: " + retour)

        assert test == retour

        info("*" * 15)
        print("  ")

    info("*" * 30)
    info("*" * 30)
