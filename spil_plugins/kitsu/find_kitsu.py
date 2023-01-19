# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterable, List, Set
from pprint import pformat

from spil import Finder, SpilException, Sid

from spil_plugins.kitsu.connect_gazu import connect
from spil_kitsu_conf import field_mappings, type_mapping, value_mappings, defaults_by_basetype  # type: ignore

from spil.util.log import DEBUG, get_logger, INFO

log = get_logger("spil_kitsu")


class FindInKitsu(Finder):
    """
    Finder Implementation for Kitsu backend.

    TODO:
    This is work in progress / proof of concept, and is not production ready.
    Implementation must be completely overhauled.
    """

    def __init__(self):
        connect()

    def do_find(self, search_sids: List[Sid],
                as_sid: bool = True) -> Iterable[Sid] | Iterable[str]:
        """
        Yields Sids (if as_bool is True, the default) or strings (if as_bool is set to False),
        as found in Shotgrid by querying the given search_sids.

        Args:
            search_sids: A list of Typed Search Sids
            as_sid: If True (default) SId objects are yielded, else Strings.

        Returns:
            Iterable over Sids or strings.
        """

        found: Set = set()

        if not search_sids:
            log.warning('Nothing Searchable. ')

        for search_sid in search_sids:

            # TODO: call core per type, edit core for "*"

            for sid in  # self.kitsu_request(search_sid):
                if sid not in found:
                    found.add(sid)
                    if as_sid:
                        yield Sid(sid)
                    else:
                        yield sid



if __name__ == "__main__":

    log.setLevel(INFO)

    search = 'hamlet/a,s/*/*/*'

    finder = FindInKitsu()

    for f in finder.find(search):
        print(f)

    for f in finder.find(search):
        print(f)

