"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, Mapping, Any, List, overload, Optional, Callable, Dict
from typing_extensions import Literal

from spil import Sid
from spil.sid.read.util import first
from spil.sid.read.getter import Getter

from spil.util.log import debug, info, warning, error
from spil.conf import get_getter_for  # type: ignore
from spil.util.caching import lru_cache as cache
from spil.sid.read.tools import unfold_search


# @cache
def get_getter(
    sid: Sid | str, attribute: Optional[str] = None, config: Optional[str] = None
) -> Getter | None:
    """
    Calls spil.conf.get_getter_for() which is implemented in the spil_data_conf.

    Retrieves, for a given Search Sid and configuration name, the appropriate Getter and returns it.

    This typically returns a Getter depending on the Type of the Sid.
    See similar use in FindInAll and get_finder_for

    Technical note: the result is cached.
    This means that the choice of the Getter is cached, not the resulting data itself.
    The Getter is called again each time a query method (get(), get_one(), get_attr()) is called.

    Args:
        attribute:
        sid: the Search Sid for which we want to get the appropriate Getter instance
        config: an optional configuration name, to be able to have multiple configs co-existing.

    Returns:
        the Getter to use for this Search Sid

    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        warning(f'Sid could not be instanced, likely a configuration error. "{sid}" -> {_sid}')
    source = get_getter_for(_sid, attribute=attribute, config=config)
    if source:
        debug(f'Getting data source for "{sid}" {attribute or ""} {config or ""}): -> {source}')
        return source
    else:
        warning(f'Data Source not found for Sid "{sid}" ({_sid.type})')
        return None


class GetFromAll(Getter):  # noqa
    """
    This Getter will call other Getters, as configured, depending on the search sids type.

    The do_get() method is delegated to other Getters, and not implemented.
    """

    def __init__(self, config: Optional[str] = None):
        """
        Config is an argument that will be passed to the config, via get_getter_for(sid, config).
        Config acts like a key, to allow multiple GetFromAll configurations to co-exist.

        Args:
            config: name of a configuration
        """
        self.config = config

    def get(
        self,
        search_sid: str | Sid,
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        See Getter.

        """
        # we start by unfolding
        search_sids: List[Sid] = unfold_search(search_sid)

        # Dictionary to map a Getter to a list of Sids it should get.
        getter_to_searches: Dict[Getter, List[Sid]] = {}

        for search_sid in search_sids:

            # Getter for the specific search
            getter = get_getter(
                search_sid, config=self.config
            )  # IDEA: allow multiple getters to cumulate data

            if getter:
                searches = getter_to_searches.get(getter) or []
                searches.append(search_sid)
                getter_to_searches[getter] = searches
            else:
                warning(f"No Getter configured for {search_sid}. Skipped from search.")

        for getter, searches in getter_to_searches.items():

            debug(f'Searching "{getter}" --> "{searches}"')
            generator = getter.do_get(searches, attributes=attributes, sid_encode=sid_encode)

            # TODO: check if doublon check is needed
            yield from generator

    def get_data(
        self, sid: str | Sid, attributes: Optional[List[str]] = None, sid_encode: Callable = str
    ) -> Mapping[str, Any]:
        """
        See Getter

        """
        # Getter for the specific sid
        source = get_getter(sid, config=self.config)
        if source:
            return source.get_data(sid, attributes=attributes, sid_encode=sid_encode)
        else:
            error(f"No Getter for get_data() found for {sid} / config: {self.config}")
            return {}

    def get_attr(self, sid: str | Sid, attribute: str) -> Any | None:
        # Getter for the specific sid and attribute
        source = get_getter(sid, attribute=attribute, config=self.config)
        if source:
            return source.get_attr(sid, attribute=attribute)
        else:
            error(
                f"No Getter for get_attr() found for {sid} and {attribute} - config: {self.config}"
            )
            return None

    def __str__(self):
        return f'[spil.{self.__class__.__name__} -- Config: "{self.config}"]'


if __name__ == "__main__":
    print(GetFromAll())
