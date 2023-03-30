"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
import string

from typing import List, Iterable

from spil.util.log import info, debug
from spil.util.exception import SpilException
from spil.conf import sid_templates, leaf_keys  # type: ignore
from spil.sid.core.sid_resolver import sid_to_dicts
from spil import Sid
from spil.util.caching import lru_cache as cache


def extrapolate(sids: Iterable[str], as_sid: bool = False) -> Iterable[str | Sid]:
    """
    From an iterable containing leaf node paths, extrapolates all the subnode paths.

    This is useful when the data source quickly provides leaves only, and we want to construct child data.

    For example: the path "TEST/A/CHR/HERO/MOD/V001/W/avi"
    will generate: "TEST/A/CHR/HERO/MOD/V001/W", "TEST/A/CHR/HERO/MOD/V001", "TEST/A/CHR/HERO/MOD", etc.
    until "TEST".

    This is a pure string operation.

    Is as_sid is True, returns Sids instead of strings (the default). Sids are a bit slower.

    :param as_sid: if we want the returned values to be Sids, instead of strings.
    :param sids: generator
    :return:
    """

    debug(
        "Start Extrapolate {}".format(sids)
    )  # TODO: warning if a string or Sid is given, need iterable.

    generated = set()

    for sid in sids:

        sid = str(sid)

        generated.add(sid)
        if as_sid:
            yield Sid(sid)
        else:
            yield sid

        parts = sid.split("/")  # use sip
        for i, key in enumerate(reversed(parts[:-1]), 1):
            new_sid = "/".join(parts[: -1 * i])
            if new_sid in generated:
                break
            else:
                generated.add(new_sid)
                # print(new_sid)
                if as_sid:
                    yield Sid(new_sid)
                else:
                    yield new_sid


def expand(sid: str | Sid, do_extrapolate: bool = False) -> List[Sid]:
    """
    "Expand" means replacing a double wildcard "/**" by the possible amount of simple wildcards "/*", wherever possible.
    This allows for simpler searches on multiple types.

    Example:
        To find all movie files from a shot, we need to search for: hamlet/s/sq010/sh0020/*/*/*/mov
        hamlet/s/sq010/sh0020/**/mov is a simpler form.

    By default, expand only returns leaf types (do_extrapolate=False)
    hamlet/s/sq010/sh0020/** will be expanded to files, eg hamlet/s/sq010/sh0020/*/*/*/* and hamlet/s/sq010/sh0020/*/*/*/*/*

    If do_extrapolate is True, expand will return all possible intermediate types.
    Eg. hamlet/s/sq010/sh0020/** will also be expanded to hamlet/s/sq010/sh0020 (shot), and hamlet/s/sq010/sh0020/* (task), etc.
    This is not the default behaviour.

    This function expects a string (or sid) and converts to a list of typed Sids.

    Note: if there is nothing to expand (no "/**" in the string),
    the string is typed as-is (calling "simple_typing(sid)"), to return a list of typed Sids.

    Expand can only receive "typeable" sids:
    Aliases and "or" syntax are not allowed (they are handled before).

    Expand works like this:

    - First we get the root of the given Sid, before the "/**".
    We get the roots basetype ("asset", or "shot", etc) and deduce the "leaf" key.
    The leaf key is the last key we look up.

    - Then we look up all existing types (sid_templates).
    For each type, we get the amount of keys, and replace "/**" by "/*" x the amount of keys.
    That gives us a test sid, that we use to instantiate valid sids, using all possible templates again.

    - we continue with all the types we have not already tested.

    :param sid: string (or sid)
    :param do_extrapolate: boolean
    :return: List of typed Sids
    """

    debug(f"Expanding {sid}")
    sid = str(sid)

    if not sid.count("/**"):  # nothing to expand
        r = simple_typing(sid)
        debug("Nothing to expand for {}. Just casting to Sid set {}".format(sid, r))
        return r

    if sid.count("/**") > 1:
        raise SpilException("Can only expand once in a Sid.")

    if sid.count("?"):  # sid contains Query ending. We put it aside, and later append it back
        sid, query = sid.split("?", 1)
    else:
        query = ""

    root = sid.split("/**")[0]
    basetype = Sid(root).basetype
    debug("Basetype: {}".format(basetype))
    if not basetype:
        raise SpilException(
            f'The Search Sids "{sid}" root "{root}" cannot be typed, so it cannot be expanded. This is probably a configuration error.'
        )

    leaf_key = leaf_keys.get(basetype)
    # leaf_key = 'version'  # TODO: find an option to edit this depending on the Finder.
    if not do_extrapolate and not leaf_key:
        raise SpilException(
            f'Leaf key not defined for basetype: "{basetype}". Please check config.'
        )

    tested = []
    found = []
    result = []
    for key, template in sid_templates.items():
        debug("Checking " + key)
        if key in found:
            debug(".. Already checked {}, continue".format(key))
            continue
        debug(f'.. Checking key "{key}"')
        keys = list(string.Formatter().parse(template))
        if do_extrapolate or keys[-1][1] == leaf_key:
            count = len(keys) - 1
            current = sid.count("/")
            needed = count - current + 1
            test = sid.replace("/**", "/*" * needed)
            if test in tested:
                debug("... Already tested, continue")
                continue
            else:
                tested.append(test)
            debug("... Filled {}x* --> {}".format(needed, test))
            matching = sid_to_dicts(test)
            debug("... Got {}".format(matching))
            for __type, data in matching.items():
                debug(".... found :" + __type)
                found.append(__type)
                if data and (do_extrapolate or (list(data)[-1] == leaf_key)):
                    if query:
                        new_sid = Sid("{}:{}?{}".format(__type, test, query))
                    else:
                        new_sid = Sid(__type + ":" + test)
                    debug(".... appending: {}".format(new_sid.uri))
                    result.append(new_sid)
        else:
            debug('.. Type "{}" is not a leaf, and do_extrapolate is False, skipped.'.format(key))
            continue

    return sorted(list(set(result)))


@cache
def simple_typing(sid: str | Sid) -> List[Sid]:
    """
    Takes a given sid string (or Sid), typically containing search symbols, and returns a list of typed Sids.
    If the sid cannot be typed, returns a list with Sid(sid) inside.

    Args:
        sid:

    Returns:

    """
    _sid = str(sid)

    if _sid.count("?"):  # sid contains Query ending. We put it aside, and later append it back
        _sid, query = _sid.split("?", 1)
    else:
        query = ""

    root = _sid.split("/*")[0]
    basetype = Sid(root).basetype
    if not basetype:  # not typed, returning as is
        return [Sid(sid)]
        # raise SpilException('The Search Sids "{}" root "{}" cannot be typed, so it cannot be expanded. This is probably a configuration error.'.format(sid, root))

    result = []
    matching = sid_to_dicts(_sid)
    debug("Got {}".format(matching))
    for __type, data in matching.items():
        debug("found :" + __type)
        if query:
            new_sid = Sid("{}:{}?{}".format(__type, _sid, query))
        else:
            new_sid = Sid(__type + ":" + _sid)
        debug("appending: {}".format(new_sid.uri))
        result.append(new_sid)

    return list(set(result)) or [Sid(sid)]


if __name__ == "__main__":
    from pprint import pprint
    from spil import setLevel
    from spil.util.log import DEBUG

    setLevel(DEBUG)

    sid = "hamlet/**"
    r = expand(sid)
    pprint(r)
