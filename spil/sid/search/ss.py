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

import os
import six
import glob

from spil import conf
from spil.sid.search.transformers import extensions, or_op, expand, transform
from spil.sid.sid import Sid
from sid_conf import sip
from spil.util.exception import SpilException
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

    def get(self, search_sid):
        """
        Search dispatcher.

        :param search_sid:
        :return:
        """
        # we start by transforming
        list_search_transformers = [extensions, or_op, expand]
        search_sids = transform(search_sid, list_search_transformers)

        # depending on input, select the right generator
        is_qm_search = any([ssid.count('?') for ssid in search_sids])
        is_sorted_search = any([ssid.count('>') for ssid in search_sids])

        if is_qm_search and is_sorted_search:
            raise NotImplementedError('Currently no multi search implemented.')

        if is_sorted_search:
            generator = self.sorted_search(search_sids)

        elif is_qm_search:
            if search_sids[0].endswith('?'):  # FIXME: check coherence
                generator = self.star_search(search_sids)
            else:
                generator = self.qm_search(search_sids)
        else:
            generator = self.star_search(search_sids)

        for i in generator:
            yield i

    def qm_search(self, search_sids):
        """
        Question mark search.

        :param search_sids:
        :return:
        """
        founds = list()
        for search_sid in search_sids:
            ssid = str(search_sid).replace('?', '*')
            debug('star search start on {}'.format(ssid))
            founds.extend(self.star_search([ssid], as_sid=False))
            debug('star search done')

        debug('Sorting')
        founds = sorted(list(set(founds)))  # More efficient here, then to presort all before
        debug('Done Sorting')

        done = set()
        done_add = done.add  # performance
        for search_sid in search_sids:
            index = str(search_sid).split('/').index('?')
            for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index+1]):
                sid = Sid(sip.join(key))
                if sid not in done:  # there can be redundant results, for example "ma,mb" extensions
                    done_add(sid)
                    yield sid

    def sorted_search(self, search_sids):
        """
        Operates a sorted search.
        A sorted search contains the ">" sign, standing for "last"
        or the "<>" sign, standing for "first". (not yet implemented)

        :param search_sids:
        :return:
        """
        # FIXME: check if index is coherent in all search_sids
        index = str(search_sids[0]).split('/').index('>')
        # indices = [i for i, x in enumerate(str(search_sid).split('/')) if x == '>']
        # debug index, indices

        founds = list()
        for search_sid in search_sids:
            ssid = str(search_sid).replace('>', '*')
            debug('star search start on {}'.format(ssid))
            founds.extend(self.star_search([ssid], as_sid=False))
            debug('star search done')

        founds = sorted(list(set(founds)), reverse=True)
        # TODO: sort by row - and resort after each narrowing
        #pprint(founds)
        debug('found {} matches'.format(len(founds)))

        # works with > in any position, but does not use sort by row, and no delegate sorting, and no special sorting
        for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
            result = list(grp)
            # debug('{}: {}'.format(key, result))
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
