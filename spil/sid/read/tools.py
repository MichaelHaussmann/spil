"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR a PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import List, Callable
from pprint import pformat

from spil import Sid
from spil.util.caching import lru_kw_cache as cache
from spil.util.log import warn, debug, error

from spil.sid.read.unfolders.extensions import execute as extensions
from spil.sid.read.unfolders.or_op import execute as or_op
from spil.sid.read.unfolders.expand import execute as expand
from spil.sid.read.unfolders.typed_narrow import execute as narrow
from spil.sid.read.unfolders.extrapolate import execute as extrapolate

# "unfolders" by execution order for existing searches
list_search_unfolders = [extensions, or_op, expand, narrow]

# FIXME: at some point we will probably need to automatically narrow the searches.
# Currently, multiple types can have identical search sids, which may lead to multiple useless runs.


def apply_unfolders(sid: str, unfolders: List[Callable]) -> List[Sid]:
    """
    Takes the given sid, executes Search Sid "unfolders" (functions)
    and returns a sorted list of unique search sids.

    "Unfolder" functions takes a list of search sids, and returns a list of search sids.

    Note: (#FIXME: this has to be refactored with explicit typing)
        The unfolder function list is: [extensions, or_op, expand, narrow]
        "extension" and "or_op" operate on lists of strings
        "expand" gets strings and returns Sid objects
        "narrow" gets Sids and returns Sids.

    Args:
        sid: a search Sid string
        unfolders: a list of callables getting a list of Sids and returning a List of Sids.

    Returns: A sorted list of unique Sid objects.

    """
    result = [sid]
    for func in unfolders:
        done = func(result)
        result = done

    return sorted(set(result))


@cache
def unfold_search(
    search_sid: str | Sid, do_uniquify: bool = False, do_extrapolate: bool = False
) -> List[Sid]:
    """
    This function transforms an untyped "search sid",
    (a Sid or string containing search signs, like "*", "**" or ",")
    into a list of typed search Sid objects.

    If do_extrapolate is True, all intermediate types are included in the result.
    Intermediate types are all the parent types of the given one (the upstream hierarchy).

    If do_uniquify is True, duplicate Sids that share the same string are removed.
    This is only useful for testing.

    Examples:
        >>> unfold_search("hamlet/s,a")
        [Sid('asset:hamlet/a'), Sid('shot:hamlet/s')]

        >>> unfold_search("hamlet/s,a/*")
        [Sid('asset__assettype:hamlet/a/*'), Sid('shot__sequence:hamlet/s/*')]

        >>> unfold_search("hamlet/s,a/*", do_extrapolate=True)
        [Sid('project:hamlet'), Sid('asset:hamlet/a'), Sid('asset__assettype:hamlet/a/*'), Sid('shot:hamlet/s'), Sid('shot__sequence:hamlet/s/*')]

        >>> unfold_search("*/*/*")
        [Sid('asset__assettype:*/a/*'), Sid('shot__sequence:*/s/*')]

        >>> unfold_search("hamlet/*/**/maya")
        [Sid('asset__file:hamlet/a/*/*/*/*/*/ma'), Sid('asset__file:hamlet/a/*/*/*/*/*/mb'), Sid('shot__file:hamlet/s/*/*/*/*/*/ma'), Sid('shot__file:hamlet/s/*/*/*/*/*/mb')]

        >>> unfold_search("hamlet/a/char/ophelia/rig")
        [Sid('asset__task:hamlet/a/char/ophelia/rig')]

    It also applies uris if present and if appliable:
        >>> unfold_search("hamlet/s/**/movie?version=>")
        [Sid('shot__movie_file:hamlet/s/*/*/*/>/*/avi'), Sid('shot__movie_file:hamlet/s/*/*/*/>/*/mov'), Sid('shot__movie_file:hamlet/s/*/*/*/>/*/mp4')]

    Args:
        search_sid: a search sid (Sid object or string)
        do_uniquify: if True remove duplicates with same string from the result. For testing purposes only.
        do_extrapolate: if True, include intermediate types in the result.

    Returns: a list of Sid objects
    """

    debug('Treating Search Sid: "{}"'.format(search_sid))

    # unfolding
    search_sids = apply_unfolders(
        str(search_sid), list_search_unfolders + ([extrapolate] if do_extrapolate else [])
    )

    # removing invalid
    for ssid in search_sids.copy():  # make this a search unfolder ?
        if not ssid:  # untyped Sid evaluates to False
            search_sids.remove(ssid)
        if ssid.string.count("?"):  # Un-appliable Query (query still present in string)
            warn(f'SearchSid "{ssid}" is typed, but has un-applied Query. Cannot be searched.')
            search_sids.remove(ssid)

    if do_uniquify:
        search_sids = uniquify_searches(search_sids)

    debug(f'Done "{search_sid}" - Unfolded {len(search_sids)} --> {pformat(search_sids)}')

    return search_sids


def uniquify_searches(search_sids: List[Sid]) -> List[Sid]:
    """
    For a list of Sids, removes duplicates having the same string representation.

    This is experimental, and should not be used in normal usage.
    Can be used during tests.

    Args:
        search_sids: a list of Sids that may contain search signs ("*", etc.)

    Returns: a new list with duplicates removed.

    """
    done = set()
    result = []
    for ssid in search_sids:
        if ssid.string not in done:
            done.add(ssid.string)
            result.append(ssid)

    return result


if __name__ == "__main__":

    from logging import FATAL
    from pprint import pprint
    from spil.util.log import setLevel, info

    info("Tests start")

    setLevel(FATAL)

    searches = {}
    searches["hamlet"] = "One project"
    searches["*"] = "All projects"
    searches["hamlet/*"] = "One project, all types "
    searches["*/s"] = "all project, one type"
    searches["*/a"] = "all project, one type"
    searches["*/s,a"] = "all project, some types"
    searches["hamlet/s,a"] = "one project, some types"
    searches["*/s,a/*"] = "all project, some types, cats / seqs"
    searches["hamlet/s,a/*"] = "one project, some types, cats / seqs"
    searches["*/*"] = "all project, all types"
    searches["*/*/*"] = "all project, all types, cats / seqs"
    searches["hamlet/a,s/*/*"] = "one project, until shots / assets"
    searches["*/*/*/*"] = "all project, until shots / assets"

    searches["hamlet/s/*/*/*"] = "one project until shot tasks"
    searches["hamlet/s/**/movie"] = "one project all shot movies"
    searches["hamlet/s/**/movie?version=>"] = "one project all shot movies, last version"
    searches["hamlet/s/**"] = ""
    searches["hamlet/*/**"] = ""
    searches["hamlet/*/**/maya"] = ""

    for test in searches.keys():

        results = unfold_search(test)
        print(test + " -->")
        pprint(results)

        results = unfold_search(test, do_extrapolate=True)
        print(test + " -->")
        pprint(results)

        print("=" * 10)
