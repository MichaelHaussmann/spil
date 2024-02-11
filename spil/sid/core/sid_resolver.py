"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Tuple, List, Optional

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
    Parses a given "sid" string using the existing spil_sid_config templates.
    If "_type" is given, only the template named after the given "_type" is parsed.
    Else, all templates are parsed, and the first matching result is returned.
    This is the normal usage (as opposed to sid_to_dicts which returns all possible results).

    Returns a tuple with the type and the resolved data dict.
    If the parsing failed (no template matching) returns a (None, None) tuple.

    The function is wrapping resolva.Resolver.

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

    return template, data


@cache
def sid_to_dicts(sid: str) -> dict[str, dict]:
    """
    Parses a given "sid" using the existing spil_sid_config templates.
    Returns a dict with the types and the resolved data.

    This function parses all templates, and data from all matching templates are returned.
    This usage is not standard (as opposed to sid_to_dict which returns the first matching data).
    It makes sense only for broad read sids (including /**) where we want to catch-all types.

    If no match is found, an empty dict is returned.

    This function wraps resolva.Resolver.resolve_all.

    Args:
        sid: a Sid string

    Returns:
        a dictionary containing types as keys and resolved data as values.

    """
    r = Resolver.get("sid")

    return r.resolve_all(sid)


def dict_to_sid(data: dict, _type: Optional[str] = None) -> str:
    """
    Formats the given "data" dictionary using the given template "_type".
    If "_type" is not given it is detected using "dict_to_type".

    Returns the sid string.

    Args:
        data: a data dictionary with Sid fields
        _type: a Sid type name, which is the key to the template in spil_sid_conf.

    Returns: a Sid string, or an empty string if the data does not match any template.

    """
    if not data:
        raise SpilException("[dict_to_sid] Data is empty")

    r = Resolver.get("sid")

    if _type:
        result = r.format_one(data, _type)
    else:
        name, result = r.format_first(data)

    return result or ""


def dict_to_type(data: dict, all: bool = False) -> str | List[str]:
    """
    Retrieves the sid types for the given dict "data".
    "data" can be unsorted.

    If "all" is False (default), the first matching type is returned.
    If "all" is set to True, of list of corresponding types is returned,
    although usually a single type should match.

    Multiple matching types may be a sign for a configuration problem.
    It is logged using debug('Sid multitypes for  =>')

    The types are found by calling resolva.Resolver.format_all.
    Note that we always use "format_all".
    Even if "all" is False, we do not use "format_first".
    Because we want to log that multiple types where found.

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
