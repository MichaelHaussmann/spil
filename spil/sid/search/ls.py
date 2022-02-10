# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import re
import itertools as it

from sid_conf import sip
from spil.sid.search.ss import SidSearch
from spil.sid.sid import Sid
from spil.util.log import debug, info, warn


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
    until "TEST"

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


class LS(SidSearch):
    """
    List search.

    Searches for sids from a Sid string list.
    The search list is given during object instantiation.

    The search list can optionnaly be extrapolated

    Implements a glob like "star_search".
    This loops through the list and accumulates the matching results.



    Note: searchlist can be a generator, but it will be exhausted after a single function call.

    Still alpha.

    """
    def __init__(self, searchlist, do_extrapolate=False, do_pre_sort=False, do_strip=False):
        """
        Sets the search list, a list of sid strings.

        Note: searchlist can be a generator, but it will be exhausted after a single function call.

        :param searchlist:
        :param do_extrapolate:
        :param do_pre_sort:
        :param do_strip: if the returned items should be strip() (typically if coming from file input)
        """
        if do_extrapolate:
            self.searchlist = extrapolate(searchlist)
        else:
            self.searchlist = searchlist

        self.is_searchlist_sorted = False

        if do_pre_sort:
            self.sort_searchlist()

        self.do_strip = do_strip

    def sort_searchlist(self):
        self.searchlist = sorted(list(set(self.searchlist)))
        debug('Pre-sorted {} sids'.format(len(self.searchlist)))
        self.is_searchlist_sorted = True

    def get_searchlist(self, do_sort=False):
        if do_sort and not self.is_searchlist_sorted:
            self.sort_searchlist()
        return self.searchlist
        # return (i for i in self.searchlist)  # new generator because list is used multiple times.

    def star_search(self, search_sids, as_sid=False, do_sort=False):
        """
        Simple star search.

        Transforms the pattern into a regex (like fnmatch.translate), but without traversing "/" (the sid separator).

        :param search_sids:
        :param as_sid:
        :param do_sort:
        :return:
        """
        done = set()
        done_add = done.add  # performance

        search_list = self.get_searchlist(do_sort=do_sort)

        for search_sid in search_sids:

            pattern = glob2re(str(search_sid))
            debug('[star_search] "{}"'.format(search_sid))

            for item in search_list:
                if re.match(pattern, item):
                    # debug('match : {}'.format(item))
                    if item not in done:
                        done_add(item)
                        if self.do_strip:
                            item = item.strip()
                        if as_sid:
                            yield Sid(item)
                        else:
                            yield item
                    else:
                        debug('{} was already found, skipped. '.format(item))


if __name__ == '__main__':

    pass
