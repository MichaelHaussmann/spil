# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import itertools as it

from spil.sid.search.util import first
from spil.sid.search.transformers import extensions, or_op, expand, transform
from spil.sid.sid import Sid
from spil.util.log import debug, warn, info


class SidSearch(object):
    """
    Interface for Sid Search sources.

    Implements common public Sid Search methods "get", "get_one", and "exists"

    """

    def __init__(self):
        """
        #TODO
        - more iterators where possible
        - better control over string / Sid
        - better algorithms

        2) allow Sid list.
        Don't know if that makes sense.

        """
        pass

    def star_search(self, search_sids, **kwargs):
        raise NotImplementedError('SidSearch is an abstract class. Please use FS or LS.')

    def get(self, search_sid, as_sid=True):
        """
        gets the Sids found using the given search_sid.
        Returns a generator over Sids, if as_sid is True (default), or over Sid strings.

        The search process is as follows:
        - the search sid string is "transformed" into a list of typed search Sids.
        - depending on the types of searches, defined by the search symbols ('>', ...), the search is delegated to a search function.
        (currently either "sorted_search" or "star_search").

        :param search_sid: string
        :param as_sid:
        :return: Sid or string
        """
        # we start by transforming
        list_search_transformers = [extensions, or_op, expand]  # uri_apply is removed, because uri is automatically applied bu Sid()
        search_sids = transform(str(search_sid), list_search_transformers)

        for ssid in search_sids[:]:  # make this a search transformer?
            if ssid.string.count('?'):
                warn('SearchSid "{}" has un-applied URI and cannot be searched. Skipped'.format(ssid))
                search_sids.remove(ssid)

        # depending on input, select the right generator
        is_sorted_search = any([ssid.string.count('>') for ssid in search_sids])

        if not search_sids:
            warn('Nothing Searchable. ')
            generator = ()
        elif is_sorted_search:
            generator = self.sorted_search(search_sids, as_sid=as_sid)
        else:
            generator = self.star_search(search_sids, as_sid=as_sid)

        for i in generator:
            yield i

    def get_one(self, search_sid, as_sid=True):
        """
        Returns the first Sid found using the given search_sid.

        Returns a Sid, if as_sid is True (default), or a Sid strings.

        Internally calls "first" on "get".

        :param search_sid: string
        :param as_sid:
        :return: Sid or string
        """

        found = first(self.get(search_sid, as_sid=False))  # search is faster if as_sid is False
        if as_sid:
            return Sid(found)
        else:
            return found

    def exists(self, search_sid):
        """
        Returns True if the given search_sid returns a result.
        Else False.

        Internally calls "bool" on "first" on "star_search".

        :param search_sid: string
        :return: True or False
        """
        return bool(first(self.star_search([search_sid], as_sid=False)))

    def sorted_search(self, search_sids, as_sid=False):
        """
        Operates a sorted search.
        A sorted search contains the ">" sign, standing for "last"
        or the "<" sign, standing for "first". (not yet implemented)

        TODO: "meaningful sort" (eg. LAY < ANI < RND), currently only alphanumerical sort.

        :param search_sids:
        :param as_sid:
        :return:
        """
        # index is coherent in all search_sids, which is a bit strange
        index = str(search_sids[0]).split('/').index('>')

        """
        indices = []
        for ss in search_sids:
            indices.append(str(ss).split('/').index('>'))
        print('ind' + str(indices))
        indices = list(set(indices))
        """
        # indices = [i for i, x in enumerate(str(search_sid).split('/')) if x == '>']
        # debug index, indices

        founds = list()
        for search_sid in search_sids:
            ssid = search_sid.full_string.replace('>', '*')
            debug('star search start on {}'.format(ssid))
            founds.extend(self.star_search([Sid(ssid)], as_sid=False))
            debug('star search done')

        founds = sorted(list(set(founds)), reverse=True)
        # TODO: sort by row - and resort after each narrowing
        #pprint(founds)
        debug('found {} matches'.format(len(founds)))

        #for index in indices:
        # works with > in any position, but does not use sort by row, and no delegate sorting, and no special sorting
        for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
            result = list(grp)
            # debug('{}: {}'.format(key, result))
            if as_sid:
                yield Sid(result[0])
            else:
                yield result[0]

        """
        for index in indices:
            if not founds:
                break
            filtered = []
            for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
                result = list(grp)
                debug('{}: "{}" {}'.format(key, result[0].split('/')[index], result))
                filtered.append(result[0])
                filtered.extend(result)
            founds = filtered
        """

        """
        for index in indices:
            for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
                result = list(grp)
                debug('{}: "{}" {}'.format(key, result[0].split('/')[index], result))
        """


    """
    Problem:

    FTOT/S/SQ0001/SH0020/**/cache,maya?state=WIP&version=>
    Doesn't return FTOT/S/SQ0001/SH0020/ANI/V019/WIP/CAM/abc
    See tests/filesearch.

    """
