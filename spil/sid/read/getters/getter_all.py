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
from typing import Iterable, List, Dict, Optional, overload, Any, Iterator, Mapping
from typing_extensions import Literal

from spil import Sid
from spil.sid.read.util import first
from spil.sid.read.getter import Getter

from spil.util.log import debug, info, warning, error
from spil.conf import get_getter_for  # type: ignore
from spil.util.caching import lru_cache as cache


@cache
def get_getter(sid: Sid | str, config: Optional[str] = None) -> Getter | None:
    """
    Calls spil.conf.get_getter_for() which is implemented in the spil_data_conf.

    Retrieves, for a given Search Sid and configuration name, the appropriate Getter and returns it.

    This typically returns a Getter depending on the Type of the Sid.
    See similar use in FindInAll and get_finder_for

    Technical note: the result is cached.
    This means that the choice of the Getter is cached, not the resulting data itself.
    The Getter is called again each time a query method (get(), get_one(), get_attr()) is called.

    Args:
        sid: the Search Sid for which we want to get the appropriate Getter instance
        config: an optional configuration name, to be able to have multiple configs co-existing.

    Returns:
        the Getter to use for this Search Sid

    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        warning(f'Sid could not be instanced, likely a configuration error. "{sid}" -> {_sid}')
    source = get_getter_for(_sid, config)
    if source:
        debug(f'Getting data source for "{sid}": -> {source}')
        return source
    else:
        warning(f'Data Source not found for Sid "{sid}" ({_sid.type})')
        return None


class GetFromAll(Getter):
    """
    This Getter will call other Getters, as configured, depending on the search sids type.

    """
    def __init__(self, config: Optional[str] = None):
        """
        Config is an argument that will be passed to the config, via get_getter_for(sid, config).
        Config acts like a key, to allow multiple GetFromAll configurations to co-exist.

        Args:
            config: name of a configuration
        """

        self.config = config

    def get(self, search_sid: str | Sid, attribute: Optional[str] = None, as_sid: bool = False) -> Iterator[Mapping[str | Sid, Any | dict]]:
        """
        For a given search, returns an Iterator over Mappings containing a Sid as key,
        and the retrieved data as value.

        By default, attribute is None, retrieved data is a dictionary containing all configured data for the Sid type.
        If attribute is given, data contains only the value of the given attribute.

        The Sids returned by Getter.get() should be identical to those returned by Finder.find().
        Getter retrieves data related to these Sids, whereas the Finder only the existing Sids themselves.

        Args:
            as_sid:
            search_sid:
            attribute:

        Returns:
            An iterator over Mappings containing a Sid as key,
            and the retrieved data as value. Either for a given attribute (attribute),
            or all data in a dictionary (data as configured).

        """
        return []

    def do_get(self, search_sids: List[Sid], attribute: Optional[str] = None, as_sid: bool = False) -> Iterator[Mapping[str | Sid, Any | dict]]:
        """
        For a given list of typed Search Sids

        Args:
            search_sids:
            attribute:
            as_sid:

        Returns:

        """
        return []

    def get_one(self, search_sid: str | Sid, attribute: Optional[str] = None, as_sid: bool = False) -> Mapping[str | Sid, Any | dict]:
        """
        Calls get() with the given parameters, and returns the first result.

        Args:
            search_sid:
            attribute:
            as_sid:

        Returns:

        """
        found = first(self.get(search_sid, attribute=attribute, as_sid=as_sid))
        return found

    def get_attr(self, search_sid: str | Sid, attribute: Optional[str] = None) -> Any | dict[str, Any] | None:
        """
        Returns the result from get_one(), but without the Sid as key.
        Returns directly the data dictionary, or the value of the attribute, if given.

        Args:
            search_sid:
            attribute:

        Returns:
        """
        result = self.get_one(search_sid=search_sid, attribute=attribute, as_sid=False)
        if result is None:
            return None
        if result.values():
            return list(result.values())[0]

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Getter())
    