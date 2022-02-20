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

from spil.sid.search.ss import SidSearch
from spil.sid.search.tools import unfold_search
from spil.sid.search.util import extrapolate
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


class LS(SidSearch):
    """
    List search.

    Searches for sids from a Sid string list.

    Still experimental.

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

    def get(self, search_sid, as_sid=True, is_unfolded=False):
        """
        Search dispatcher.

        :param search_sid:
        :param as_sid:
        :return:
        """

        # we start by transforming
        if is_unfolded:
            search_sids = [search_sid]
        else:
            search_sids = unfold_search(search_sid, do_uniquify=True)

        generator = self._get(search_sids, as_sid=as_sid)

        for i in generator:
            yield i

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
