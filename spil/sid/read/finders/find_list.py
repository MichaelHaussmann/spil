"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, List, Set

import re

from spil import Sid
from spil.sid.read.finders.find_glob import FindByGlob
from spil.sid.core.utils import extrapolate
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


class FindInList(FindByGlob):
    """
    List search.

    Searches for sids from a Sid string list.
    The search list is given during object instantiation.

    The search list can optionally be extrapolated.

    Implements a glob like "star_search".
    This loops through the list and accumulates the matching results.

    Note: searchlist can be a generator, but it will be exhausted after a single function call.

    Still beta.
    """
    def __init__(self, searchlist: List[str],
                 do_extrapolate: bool = False,
                 do_pre_sort: bool = False,
                 do_strip: bool = False):
        """
        Sets the search list, a list of sid strings.

        Note: searchlist could be a generator, but it would be exhausted after a single function call.
        If do_extrapolate is True, searchlist becomes a list.

        Args:
            searchlist:
            do_extrapolate:
            do_pre_sort:
            do_strip: if the returned items should be strip() (typically if coming from file input)
        """
        if do_extrapolate:
            self.searchlist = list(extrapolate(searchlist))
        else:
            self.searchlist = searchlist

        self.is_searchlist_sorted = False

        if do_pre_sort:
            self._sort_searchlist()

        self.do_strip = do_strip

    def _sort_searchlist(self):
        self.searchlist = sorted(list(set(self.searchlist)))
        debug('Pre-sorted {} sids'.format(len(self.searchlist)))
        self.is_searchlist_sorted = True

    def _get_searchlist(self, do_sort: bool = False) -> List[str]:
        if do_sort and not self.is_searchlist_sorted:
            self._sort_searchlist()
        return self.searchlist  # type: ignore
        # return (i for i in self.searchlist)  # new generator because list is used multiple times.

    def star_search(self, search_sids: List[Sid],
                    as_sid: bool = False,
                    do_sort: bool = False) -> Iterator[Sid] | Iterator[str]:
        """
        Simple star search.

        Transforms the pattern into a regex (like fnmatch.translate), but without traversing "/" (the sid separator).

        Args:
            search_sids:
            as_sid:
            do_sort:

        Returns:

        """
        done: Set[str] = set()
        done_add = done.add  # performance

        search_list = self._get_searchlist(do_sort=do_sort)

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

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- List: "{list(self.searchlist)[:5]}(...)"]'


if __name__ == "__main__":
    print(FindInList(['hamlet/s/sq010/sh0010/animation'], do_extrapolate=True))
