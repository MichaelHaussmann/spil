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
from typing import Iterable, List

from spil import Sid
from spil.sid.read.finder import Finder
#from spil.conf import pre_search_update
from spil.data.data import get_data_source
from spil.sid.read.tools import unfold_search

from spil.util.log import debug, info, warning, error


class FindByType(Finder):
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    def find(self, search_sid: str | Sid, as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        """
        Search dispatcher.

        The read is "unfolded" into atomic searches (from one read sid, split into a list of typed read sids).
        For each "atomic" typed read, we get the data source.

        We then group the searches by data source, to call each source with a list of searches (instead of each read individually).


        :param search_sid:
        :param as_sid:
        :return:
        """
        # we start by transforming
        search_sids = unfold_search(search_sid)

        done = set()  #TEST
        sources_to_searches = dict()

        for ssid in search_sids:

            source = get_data_source(ssid)

            if source:
                l = sources_to_searches.get(source) or list()
                l.append(ssid)
                sources_to_searches[source] = l

        for source, searches in sources_to_searches.items():

            debug('Searching "{}" --> "{}"'.format(source, searches))
            generator = source.do_find(searches, as_sid=False)

            for i in generator:
                if i not in done:  # FIXME: check why data is so often repeated, this is expensice, optimize
                    done.add(i)
                    if as_sid:
                        yield Sid(i)
                    else:
                        yield i

            else:
                warning('No data source found for "{}"'.format(ssid.full_string))

    def do_find(self, search_sids: List[Sid], as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        raise NotImplementedError("Find by Type delegates do_find to other Finders, depending on the search type.")

    def find_one(self, search_sid: str | Sid, as_sid: bool = True) -> Sid | str:
        source = get_data_source(search_sid)
        if source:
            return source.find_one(search_sid, as_sid=as_sid)

    def exists(self, search_sid: str | Sid) -> bool:
        source = get_data_source(search_sid)
        if source:
            return source.exists(search_sid)


if __name__ == "__main__":
    pass
