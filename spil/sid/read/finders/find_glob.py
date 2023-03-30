"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, List, overload, Optional

from typing_extensions import Literal

import itertools as it

from spil import Sid
from spil.sid.read.finder import Finder

from spil.util.log import debug, warning, error


class FindByGlob(Finder):
    """
    Parent class for glob type searches:
    FindInFiles, FindInList, FindInConstants

    The search process is as follows:
        find():
        - the search sid string is "unfolded" into a list of typed search Sids.

        do_find()
        - depending on the types of searches, defined by the search symbols ('>', ...), the search is delegated to a finder function.
        (currently either "sorted_search" or "star_search").
    """

    @overload
    def do_find(self, search_sids: List[Sid], as_sid: Literal[True]) -> Iterator[Sid]:  # noqa
        ...

    @overload
    def do_find(self, search_sids: List[Sid], as_sid: Literal[False]) -> Iterator[str]:  # noqa
        ...

    @overload
    def do_find(  # noqa
        self, search_sids: List[Sid], as_sid: Optional[bool]
    ) -> Iterator[Sid] | Iterator[str]:
        ...

    def do_find(self, search_sids, as_sid=True):

        # depending on input, select the right generator
        is_sorted_search = any([ssid.string.count(">") for ssid in search_sids])

        if not search_sids:
            warning("Nothing Searchable. ")
            generator = ()
        elif is_sorted_search:
            generator = self.sorted_search(search_sids, as_sid=as_sid)
        else:
            generator = self.star_search(search_sids, as_sid=as_sid)

        yield from generator

    @overload
    def star_search(
        self, search_sids: List[Sid], as_sid: Literal[False], do_sort: bool = False
    ) -> Iterator[str]:
        ...

    @overload
    def star_search(
        self, search_sids: List[Sid], as_sid: Literal[True], do_sort: bool = False
    ) -> Iterator[Sid]:
        ...

    @overload
    def star_search(
        self, search_sids: List[Sid], as_sid: Optional[bool], do_sort: bool
    ) -> Iterator[str] | Iterator[Sid]:
        ...

    def star_search(self, search_sids, as_sid=False, do_sort=False):
        msg = f'Current instance "{self}" has no star_search. FindByGlob is abstract, use FindInFiles or FindInList.'
        raise NotImplementedError(msg)

    def sorted_search(
        self, search_sids: List[Sid], as_sid: bool = True
    ) -> Iterator[Sid] | Iterator[str]:
        """
        Operates a sorted read.
        A sorted read contains the ">" sign, standing for "last"
        or the "<" sign, standing for "first". (not yet implemented)

        TODO: "meaningful sort" (eg. LAY < ANI < RND), currently only alphanumerical sort.

        :param search_sids:
        :param as_sid:
        :return:
        """
        # index is coherent in all search_sids, which is a bit strange
        index = str(search_sids[0]).split("/").index(">")

        """
        indices = []
        for ss in search_sids:
            indices.append(str(ss).split('/').index('>'))
        print('ind' + str(indices))
        indices = list(set(indices))
        """
        # indices = [i for i, x in enumerate(str(search_sid).split('/')) if x == '>']
        # debug index, indices

        founds: List[str] = []
        for search_sid in search_sids:
            ssid = search_sid.uri.replace(">", "*")
            debug("star read start on {}".format(ssid))
            founds.extend(self.star_search([Sid(ssid)], as_sid=False))
            debug("star read done")

        founds = sorted(list(set(founds)), reverse=True)
        # TODO: sort by row - and resort after each narrowing
        # pprint(founds)
        debug("found {} matches".format(len(founds)))

        # for index in indices:
        # works with > in any position, but does not use sort by row, and no delegate sorting, and no special sorting
        for key, grp in it.groupby(founds, key=lambda x: x.split("/")[0:index]):
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


if __name__ == "__main__":

    pass
