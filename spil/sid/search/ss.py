# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import itertools as it

from spil.sid.search.util import first
from spil.sid.search.transformers import extensions, or_op, expand, transform
from spil.sid.sid import Sid
from sid_conf import sip
from spil.conf import qms
from spil.util.log import debug, warn, info


class SidSearch(object):

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
        Search dispatcher.

        :param search_sid:
        :param as_sid:
        :return:
        """
        # we start by transforming
        list_search_transformers = [extensions, or_op, expand]  # uri_apply is removed, because uri is automatically applied bu Sid()
        search_sids = transform(str(search_sid), list_search_transformers)

        # depending on input, select the right generator
        is_qm_search = any([ssid.string.count(qms) for ssid in search_sids])
        is_sorted_search = any([ssid.string.count('>') for ssid in search_sids])

        if is_qm_search and is_sorted_search:
            raise NotImplementedError('Currently no multi search implemented.')

        if is_sorted_search:
            generator = self.sorted_search(search_sids)

        elif is_qm_search:
            if search_sids[0].endswith(qms):  # FIXME: check coherence
                generator = self.star_search(search_sids, as_sid=as_sid)
            else:
                generator = self.qm_search(search_sids, as_sid=as_sid)
        else:
            generator = self.star_search(search_sids, as_sid=as_sid)

        for i in generator:
            yield i

    def get_one(self, search_sid, as_sid=True):

        found = first(self.get(search_sid, as_sid=False))  # search is faster if as_sid is False
        if as_sid:
            return Sid(found)
        else:
            return found

    def exists(self, search_sid):
        return bool(first(self.star_search([search_sid], as_sid=False)))

    def qm_search(self, search_sids, as_sid=False):
        """
        Question mark search.

        We star-search all Sids that match up to the qms ("#").
        Then we check if at least one matches the complete search_sid pattern.

        This is faster than the full search, but fails to find results if the partial search is not implemented.
        In this case we invoque qm_search_full.

        :param search_sids:
        :param as_sid:
        :param do_sort:
        :return:
        """
        done = set()
        done_add = done.add  # performance

        for search_sid in search_sids:
            index = str(search_sid).split('/').index(qms)
            ssid = sip.join(str(search_sid).split('/')[0:index + 1]).replace(qms, '*')
            search_roots = self.star_search([ssid], as_sid=False)

            for root in search_roots:
                ssid = str(search_sid).replace(qms, root.split(sip)[-1])
                if first(self.star_search([ssid], as_sid=False)):
                    done_add(root)
                    continue

        if done:
            done = sorted(list(done))

            for sid in done:
                if as_sid:
                    yield Sid(sid)
                else:
                    yield sid

        else:
            info('qm_search did not find any result, invoking qm_search_full.')
            for i in self.qm_search_full(search_sids, as_sid=as_sid):
                yield i

    def qm_search_full(self, search_sids, as_sid=False):
        """
        Question mark search.

        We star search all Sids that matches the search, and then keep only the part until the qms ("#")
        (This is slower than the other qm_search function, but is needed because in some cases the faster search does not work.)

        :param search_sids:
        :param as_sid:
        :return:
        """
        done = set()  #FIXME: this is currently untested
        done_add = done.add  # performance
        for search_sid in search_sids:
            ssid = search_sid.full_string.replace(qms, '*')
            debug('star search start on {}'.format(ssid))
            founds = self.star_search([Sid(ssid)], as_sid=False)
            debug('star search done')

            index = str(search_sid).split('/').index(qms)
            for f in founds:
                sid = sip.join(f.split('/')[0:index + 1])
                if sid not in done:
                    done_add(sid)
                    if as_sid:
                        yield Sid(sid)
                    else:
                        yield sid

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
