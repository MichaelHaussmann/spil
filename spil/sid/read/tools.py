# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.util.caching import lru_kw_cache as cache
from spil.util.log import warn, debug, error

from spil.sid.read.unfolders.extensions import execute as extensions
from spil.sid.read.unfolders.or_op import execute as or_op
from spil.sid.read.unfolders.expand import execute as expand
from spil.sid.read.unfolders.typed_narrow import execute as narrow
from spil.sid.read.unfolders.extrapolate import execute as extrapolate

# unfolders by execution order for existing searches
list_search_unfolders = [extensions, or_op, expand, narrow]

# FIXME: at some point we will probably need to automatically narrow the searches.
# Currently, multiple types can have identical search sids, which may lead to multiple useless runs.


def apply_unfolders(sid, unfolders):
    """
    Takes the given sid, executes Search Sid unfolders and returns a sorted list of unique search sids.

    Each transformer takes a list of search sids strings, and returns a list of search sids strings.
    :return:
    """
    previous = [sid]
    for function in unfolders:
        done = function(previous)
        previous = done
    result = previous

    result = list(set(result))  # keep sorting ?

    return sorted(result)


@cache
def unfold_search(search_sid, do_uniquify=False, do_extrapolate=False):

    debug('Treating Search Sid: "{}"'.format(search_sid))

    # transforming
    search_sids = apply_unfolders(
        str(search_sid), list_search_unfolders + ([extrapolate] if do_extrapolate else [])
    )

    # removing invalid
    for ssid in search_sids[:]:  # make this a search transformer?
        if ssid.string.count("?"):
            warn('SearchSid "{}" has un-applied URI and cannot be searched. Skipped'.format(ssid))
            search_sids.remove(ssid)

    if do_uniquify:
        search_sids = uniquify_searches(search_sids)
    from pprint import pformat
    debug('Done "{}" - Searching {} --> {}'.format(search_sid, len(search_sids), pformat(search_sids)))

    return search_sids


def uniquify_searches(search_sids):

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

    searches = dict()
    searches["FTOT"] = "One project"
    searches["*"] = "All projects"
    searches["FTOT/*"] = "One project, all types "
    searches["*/S"] = "all project, one type"
    searches["*/A"] = "all project, one type"
    searches["*/S,A"] = "all project, some types"
    searches["FTOT/S,A"] = "one project, some types"
    searches["*/S,A/*"] = "all project, some types, cats / seqs"
    searches["FTOT/S,A/*"] = "one project, some types, cats / seqs"
    searches["*/*"] = "all project, all types"
    searches["*/*/*"] = "all project, all types, cats / seqs"
    searches["FTOT/A,S/*/*"] = "one project, until shots / assets"
    searches["*/*/*/*"] = "all project, until shots / assets"

    searches["FTOT/S/*/*/*"] = "one project until shot tasks"
    searches["FTOT/S/**/movie"] = "one project all shot movies"
    searches["FTOT/S/**/movie?version=>"] = "one project all shot movies, last version"
    searches["FTOT/S/**"] = ""
    searches["FTOT/*/**"] = ""
    searches["FTOT/*/**/maya"] = ""
    searches["CBM/A,S/**"] = ""
    searches["JEV/A,S/**"] = ""
    searches = dict()
    searches["JEV/*/**"] = ""

    for test in searches.keys():

        results = unfold_search(test, do_uniquify=True)
        print(test + "-->")
        pprint(results)

        results = unfold_search(test, do_extrapolate=False)
        print(test + "-->")
        pprint(results)

        print("*" * 10)
