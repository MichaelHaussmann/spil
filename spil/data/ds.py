# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import six

from spil import Sid
#from spil.conf import pre_search_update
from spil.util.log import debug, warn, info, error

from spil.data.data import get_data_source
from spil.sid.search.ss import SidSearch
from spil.sid.search.util import first
from spil.sid.search.tools import unfold_search


class Data(SidSearch):
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    def get(self, search_sid, as_sid=True):
        """
        Search dispatcher.

        The search is "unfolded" into atomic searches (from one search sid, split into a list of typed search sids).
        For each "atomic" typed search, we get the data source.

        We then group the searches by data source, to call each source with a list of searches (instead of each search individually).


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

        for source, searches in six.iteritems(sources_to_searches):

            debug('Searching "{}" --> "{}"'.format(source, searches))
            generator = source.get(searches, as_sid=False, is_unfolded=True)

            for i in generator:
                if i not in done:  # FIXME: check why data is so often repeated, this is expensice, optimize
                    done.add(i)
                    if as_sid:
                        yield Sid(i)
                    else:
                        yield i

            else:
                warn('No data source found for "{}"'.format(ssid.full_string))

    def get_one(self, search_sid, as_sid=True):

        found = first(self.get(search_sid, as_sid=False))  # search is faster if as_sid is False
        if as_sid:
            return Sid(found)
        else:
            return found

    def exists(self, search_sid):  # TODO: evaluate best implementation
        source = get_data_source(search_sid)
        if source:
            return source.exists(search_sid)

    def create(self, sid):
        # FIXME: this is a stub.
        return
        destination = get_data_destination(sid)
        if destination:  # and hasattr(destination, 'create'):
            return destination.create(sid)


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, ERROR

    setLevel(ERROR)
