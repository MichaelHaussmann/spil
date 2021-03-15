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
from spil.util.exception import SpilException
from spil.util.log import debug, warn


class FS(object):
    """
    File search.

    Searches for sids in a File System.

    Still experimental... barely a proof of concept.

    # TODO : more tests, better algorithms, iterators

    """
    def __init__(self):
        """
        Implementation ideas :

        1) Class hierarchy for searches (LS - FS)

        1) work with iterators.
        Makes sense for star_search and qm_search, which do not sort.
        (we could uniqfy using an itertool I suppose)
        Makes less sense with the sorted search - although the input of the sorted search can also be an iterator.

        2) allow Sid list.
        Don't know if that makes sense.

        :param search_list:
        """
        pass

    def get(self, search_sid):
        """
        Search dispatcher.

        :param search_list:
        :param search_sid:
        :return:
        """
        # we start by transforming
        list_search_transformers = [extensions, or_op, expand]
        search_sids = transform(search_sid, list_search_transformers)

        # depending on input, select the right generator
        is_qm_search = any([ssid.count('?') for ssid in search_sids])
        is_sorted_search = any([ssid.count('^') for ssid in search_sids])

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

    def star_search(self, search_sids, as_sid=True):
        """
        Simple star search.

        Uses Glob.

        :param search_sids:
        :param as_sid:
        :return:
        """
        done = set()
        done_add = done.add  # performance

        for search_sid in search_sids:

            debug('[fs_star_search] "{}"'.format(search_sid))

            search = Sid(search_sid)

            # filling intermediate values with *

            debug('Search : ' + str(search))
            debug('PATH : {}'.format(search.path))
            path = search.path

            if not path:
                warn('Search sid {} did not resolve to a path. Cancelled.'.format(search))
                return

            debug('Search path : ' + str(path))

            # TODO need a way to find a root path depending on other sid parts (eg: fx caches)
            project_path = search.get_as('project').path

            pattern = path.split(project_path + '/')[-1]

            for key, value in six.iteritems(conf.search_path_mapping):
                pattern = pattern.replace(key, value)

            debug('pattern : ' + str(pattern))
            debug('project_path : ' + str(project_path))

            if str(pattern) == str(project_path):
                warn('No valid search pattern')
                return

            """
            found = []
            for ext in pattern.split('.')[-1].split(','):
                new_pattern = pattern.split('.')[0] + '.' + ext
                found.extend(glob.glob(os.path.join(project_path, new_pattern)))
            """

            found = glob.glob(os.path.join(project_path, pattern))
            debug('found')
            debug(found)
            result = []
            for path in found:
                path = str(path).replace(os.sep, '/')
                try:
                    sid = Sid(path=path)
                    debug('found ' + str(sid))
                    for key, value in conf.path_mapping['project'].items():
                        if key == sid.get('project'):
                            sid.project = value

                except SpilException as e:
                    debug('Path did not generate sid : {}'.format(path))
                    continue
                if not sid:
                    warn('Path did not generate sid : {}'.format(path))
                    continue

                item = str(sid)
                if item not in done:
                    done_add(item)
                    if as_sid:
                        yield sid
                    else:
                        yield item

    def qm_search(self, search_sids):
        """
        Question mark search.

        :param search_sids:
        :param search_list:
        :param search_sid:
        :return:
        """
        # we get the requested types
        ssid = str(search_sids[0])  # FIXME: check if coherent in all search_sids
        parts = ssid.split('/?')
        # print(parts)
        sid_types = []
        new_ssid = ''
        for part in parts[:-1]:
            new_ssid = new_ssid + part + '/*'
            sid_types.append(list(Sid(new_ssid).data)[-1])  # FIXME: official method. Clarify Sid vocabulary (type, key, last, etc)

        # print ('Types {}'.format(key_types))

        done = set()
        for search_sid in search_sids:
            ssid = str(search_sid)
            for s in self.star_search([ssid.replace('?', '*')]):
                for sid_type in sid_types:
                    got = s.get_as(sid_type)
                    if got not in done:
                        done.add(got)
                        yield got

    def sorted_search(self, search_sids):
        """
        Operates a sorted search.
        A sorted search contains the "^" sign, standing for "last"
        or the "." sign, standing for "first". (not yet implemented)

        :param search_sids:
        :param search_sid:
        :return:
        """
        # FIXME: check if index is coherent in all search_sids
        index = str(search_sids[0]).split('/').index('^')
        # indices = [i for i, x in enumerate(str(search_sid).split('/')) if x == '^']
        # print index, indices

        founds = list()
        for search_sid in search_sids:
            ssid = str(search_sid).replace('^', '*')
            founds.extend(self.star_search([ssid], as_sid=False))

        founds = sorted(list(set(founds)), reverse=True)
        # TODO: sort by row - and resort after each narrowing
        # pprint(founds)
        print('found {} matches'.format(len(founds)))

        # works with ^ in any position, but does not use sort by row, and no delegate sorting, and no special sorting
        for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
            result = list(grp)
            # print('{}: {}'.format(key, result))
            yield result[0]

        """
        for index in indices:
            if not founds:
                break
            filtered = []
            for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
                result = list(grp)
                print('{}: "{}" {}'.format(key, result[0].split('/')[index], result))
                filtered.append(result[0])
                filtered.extend(result)
            founds = filtered
        """

        """
        for index in indices:
            for key, grp in it.groupby(founds, key=lambda x: x.split('/')[0:index]):
                result = list(grp)
                print('{}: "{}" {}'.format(key, result[0].split('/')[index], result))
        """


if __name__ == '__main__':

    pass

