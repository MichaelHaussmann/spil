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
from typing import Iterable, List, Mapping, Dict, Optional

from spil import Sid
from spil.sid.read.finder import Finder

from spil.util.log import debug, info, warning, error
from spil.conf import get_finder_for  # type: ignore
from spil.util.caching import lru_cache as cache
from spil.sid.read.tools import unfold_search


@cache
def get_finder(sid: Sid | str, config: Optional[str] = None) -> Finder | None:
    """
    For a given Sid, looks up the matching data_source, as given by config_name.
    Return value is an instance implementing Finder.

    Technical note: the result is cached.
    This means that the choice of the data source is cached, not the resulting data itself.
    The data source is called again each time a Finder() method is called.
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        warning('Sid could not be instanced, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = get_finder_for(_sid, config)
    if source:
        debug('Getting data source for "{}": -> {}'.format(sid, source))
        return source
    else:
        warning('Data Source not found for Sid "{}" ({})'.format(sid, _sid.type))
        return None


class FindInFinders(Finder):
    """
    This Finder will call other Finders, as configured, depending on the search sids type.

    """
    def __init__(self, config: Optional[str] = None):
        """
        Config is an argument that will be passed to the config, via get_finder_for(sid, config).
        Config acts like a key, to allow multiple FindInFinders configurations to co-exist.



        """
        self.config = config

    def find(self, search_sid: str | Sid, as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        """
        Search dispatcher.

        The search is "unfolded" (one possibly untyped search sid is "unfolded" into a list of typed search sids).
        For each typed search, we get the appropriate Finder.

        We then group the searches by Finder, to call each Finder with a list of searches (instead of each search individually).


        :param search_sid:
        :param as_sid:
        :return:
        """
        # we start by transforming
        search_sids = unfold_search(search_sid)

        done = set()  #TEST
        sources_to_searches: Dict[Finder, List[Sid]] = dict()

        for ssid in search_sids:

            source = get_finder(ssid, self.config)

            if source:
                l = sources_to_searches.get(source) or list()
                l.append(ssid)
                sources_to_searches[source] = l

        for source, searches in sources_to_searches.items():

            debug('Searching "{}" --> "{}"'.format(source, searches))
            generator = source.do_find(searches, as_sid=False)

            for i in generator:
                if i not in done:  # FIXME: check why data is so often repeated, this is expensive, optimize
                    done.add(i)
                    if as_sid:
                        yield Sid(i)
                    else:
                        yield i

            else:
                debug('Nothing found for "{}"'.format(ssid.full_string))

    def do_find(self, search_sids: List[Sid], as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        raise NotImplementedError("Find by Type delegates do_find to other Finders, depending on the search type.")

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'

if __name__ == "__main__":
    print(FindInFinders())
