"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Tuple, List, Optional, Mapping

import string
from collections import OrderedDict

import spil.vendor  # SMELL
import lucidity  # type: ignore
from lucidity import Template  # type: ignore

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
    if _type:
        template = Template(
            _type,
            sid_templates.get(_type) or raiser(f"resolver received an invalid type: {_type}"),
            anchor=lucidity.Template.ANCHOR_BOTH,
            default_placeholder_expression="[^/]*",
            duplicate_placeholder_mode=lucidity.Template.STRICT,
        )

        templates = [template]

    else:
        templates = []
        for name, pattern in sid_templates.items():
            template = Template(
                name,
                pattern,
                anchor=lucidity.Template.ANCHOR_BOTH,
                default_placeholder_expression="[^/]*",
                duplicate_placeholder_mode=lucidity.Template.STRICT,
            )

            templates.append(template)

    try:
        data, template = lucidity.parse(sid, templates)
        # print 'found', data, template
    except lucidity.ParseError as e:
        debug(f'Lucidity did not find a matching pattern. Type: {_type} (Message: "{e}")')
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

    # instantiating lucidity Templates
    for name, pattern in sid_templates.items():
        template = Template(
            name,
            pattern,
            anchor=lucidity.Template.ANCHOR_BOTH,
            default_placeholder_expression="[^/]*",  # allows empty keys
            duplicate_placeholder_mode=lucidity.Template.STRICT,
        )

        # try template parse
        try:
            data, template = lucidity.parse(sid, [template])
        except lucidity.ParseError as e:
            # ParseErrors are normal, we force the parsing of all the templates,
            # and not just the first that matches, as usually
            continue

        if not data:
            continue

        # Sorting the result data into an OrderedDict():
        # getting the type
        sid_type = template.name.split(sidtype_keytype_sep)[0]
        # using template to get sorted keys for this basetype
        keys = key_types.get(sid_type)
        # filter out unused keys
        keys = filter(lambda x: x in template.keys(), keys)
        # building an Ordered dict with keys in right order
        data = data.copy()
        ordered = OrderedDict()
        for key in keys:
            ordered[key] = data.get(key)
        # appending the oredered dict to the results list
        results[template.name] = ordered

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

    data = data.copy()

    if not _type:
        _type = dict_to_type(data)  # type: ignore

    pattern = sid_templates.get(_type)

    if not pattern:
        raise SpilException(f'Unable to find pattern for type: "{_type}" \nData: "{data}"')

    template = lucidity.Template(_type, pattern)

    if not template:
        raise SpilException(f"Unexpected: No template for type: {_type}")
    try:
        sid = template.format(data).rstrip(sip)
    except lucidity.error.FormatError as e:
        debug(f'Lucidity could not format the Sid. Data: {data} / type: {_type} (Message: "{e}")')
        return ""

    return sid


# SMELL - this code is obscure and should be replaced / not be used
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

    found = []
    keys = data.keys()

    # SMELL: this whole code is obscure...
    for _type, template in sid_templates.copy().items():

        template_keys = [t[1] for t in string.Formatter().parse(template) if t[1] is not None]

        if len(keys) == len(template_keys):
            if set(keys) == set(template_keys):
                ltemplate = lucidity.Template(_type, template)
                test = ltemplate.format(data)
                if test:
                    # FIXME / #SMELL : this code is plain nonsense...
                    debug("Checking matching types ... (fails are normal)")
                    a, b = sid_to_dict(test, _type)
                    if a:
                        # print _type
                        found.append(_type)

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
