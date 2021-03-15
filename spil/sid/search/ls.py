# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import re
import itertools as it

from spil.sid.search.transformers import extensions, or_op, expand, transform
from spil.sid.sid import Sid
from spil.util.log import debug


def glob2re(pat):
    """
    Translate a shell PATTERN to a regular expression.
    There is no way to quote meta-characters.

    Borrowed from here, with many thanks.
    https://stackoverflow.com/questions/27726545/python-glob-but-against-a-list-of-strings-rather-than-the-filesystem
    where it was borrowed from fnmatch.translate

    @author: https://stackoverflow.com/users/4522780/nizam-mohamed
    """

    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            #res = res + '.*'
            res = res + '[^/]*'
        elif c == '?':
            #res = res + '.'
            res = res + '[^/]'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + '\Z(?ms)'


def extrapolate(sids):
    """
    From an iterable containing leaf node paths, extrapolates all the subnode paths.

    This is useful when the data source quickly provides leaves only, but we want to find child data.

    For example: the path "TEST/A/CHR/HERO/MOD/V001/W/avi"
    will generate: "TEST/A/CHR/HERO/MOD/V001/W", "TEST/A/CHR/HERO/MOD/V001", "TEST/A/CHR/HERO/MOD", etc.
    unitl "TEST"

    :param sids: generator
    :return:
    """

    print('In Extrapolate')

    generated = set()

    for sid in sids:

        generated.add(sid)
        # print(sid)
        yield sid

        parts = str(sid).split('/')
        for i, key in enumerate(reversed(parts[:-1]), 1):
            new_sid = '/'.join(parts[:-1 * i])
            if new_sid in generated:
                break
            else:
                generated.add(new_sid)
                # print(new_sid)
                yield new_sid


class LS(object):
    """
    List search.

    Searches for sids from a Sid string list.

    Still experimental... barely a proof of concept.

    # TODO : more tests, better algorithms, iterators

    """
    def __init__(self, search_list, do_extrapolate=False):
        """
        Sets the search list, a list of sid strings.

        Implementation ideas :

        1) work with iterators.
        Makes sense for star_search and qm_search, which do not sort.
        (we could uniqfy using an itertool I suppose)
        Makes less sense with the sorted search - although the input of the sorted search can also be an iterator.

        2) allow Sid list.
        Don't know if that makes sense.

        :param search_list:
        """
        # self.search_list = uniqfy(search_list)  # FIXME : this uniqfy loops through a long list. Is it worth it ?
        if do_extrapolate:
            self.search_list = list(extrapolate(search_list))  # TODO: keep as generator
        else:
            self.search_list = search_list

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

        Transforms the pattern into a regex (like fnmatch.translate), but without traversing "/" (the sid separator).

        :param search_sids:
        :param as_sid:
        :return:
        """
        done = set()
        done_add = done.add  # performance
        for search_sid in search_sids:

            pattern = glob2re(str(search_sid))
            debug('[star_search] "{}" in {} (...)'.format(search_sid, []))  # self.search_list[:5]))

            for item in self.search_list:  # TODO: add check unique values
                if re.match(pattern, item):
                    # debug('match : {}'.format(item))
                    if item not in done:
                        done_add(item)
                        if as_sid:
                            yield Sid(item)
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
        # debug(parts)
        sid_types = []
        new_ssid = ''
        for part in parts[:-1]:
            new_ssid = new_ssid + part + '/*'
            sid_types.append(
                list(Sid(new_ssid).data)[-1])  # FIXME: official method. Clarify Sid vocabulary (type, key, last, etc)

        # debug ('Types {}'.format(key_types))

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
        # debug index, indices

        founds = list()
        for search_sid in search_sids:
            ssid = str(search_sid).replace('^', '*')
            founds.extend(self.star_search([ssid], as_sid=False))

        founds = sorted(list(set(founds)), reverse=True)
        # TODO: sort by row - and resort after each narrowing
        #pprint(founds)
        debug('found {} matches'.format(len(founds)))

        # works with ^ in any position, but does not use sort by row, and no delegate sorting, and no special sorting
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


if __name__ == '__main__':

    pass

