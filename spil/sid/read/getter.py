"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Iterator, Mapping, Any, List, Optional, Callable

from spil import Sid
from spil.sid.read.util import first
from spil.sid.read.tools import unfold_search


class Getter:
    """
    Interface for Sid Getter.

    Whereas the Finder only finds Sids, the Getter retrieves Sid(s) and its data.

    A Getter is getting from a data source.
    Eg. GetFromPaths, GetFromSG.

    The Getters work has two forms:
    Finding with data form a search sid, or Getting data from a Sid.

    1. Finding with data

      The Getter receives a Search Sid, finds the result Sid(s) and returns them together with data.
      This can be considered like a Finder including dependencies (the "Finder" itself only finds Sids).

      Implementation options

        - The Getter calls the data source directly and retrieves Sids with data in one go. Typically, it is done when the data source is a database (for example GetFromSG)

        - The Getter calls a Finder to find the Sids, and then retrieves the data for each of them. For example GetFromPaths calls FindInPaths and then reads the data from disk for the Sids.

      Methods: get(), do_get(), get_one()
      These methods yield over dicts containing the data.
      One special field named "sid" contains the Sid.

    2. Getting data

      The Getter receives a specific Sid, and retrieves its data.

      It is possible to call

        - For a given existing Sid, retrieving data with all or some attributes

        - For a given existing Sid, retrieving one attribute

      Methods: get_data(), get_attr()
      get_data() returns the data dict
      get_attr() returns the attributee

    """

    def get(
        self,
        search_sid: str | Sid,
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        For a given search, returns an Iterator over Mappings containing the retrieved data.
        One special field named "sid" contains the Sid.
        The Sid can be encoded by providing a callable to "sid_encode". Default is str.

        By default, attributes is None, retrieved data contains all configured data for the Sid type.
        If "attributes" is given, data contains only the key:value for the given attributes.

        The Sids returned by Getter.get() should be identical to those returned by Finder.find().
        Getter retrieves data related to these Sids, whereas the Finder finds only the existing Sids themselves.

        Args:
            search_sid: the search sid (possibly untyped).
            attributes: a list of attribute names, that should be fetched.
            sid_encode: a callable to which the sid object will be passed, that should return the value added to the data dictionary under the "sid" key.
                        Example: `sid_encode=lambda x: x.uri`
                        If the callable returns None, the value is not added. As in `sid_encode=lambda x: None`

        Returns:
            Iterator over Mappings containing the retrieved data.
            One special field named "sid" contains the Sid
        """
        # shortcut if Sid is not a search
        sid = Sid(search_sid)
        if sid and not sid.is_search():
            generator = self.do_get([sid], attributes=attributes, sid_encode=sid_encode)
        else:
            search_sids = unfold_search(search_sid)
            generator = self.do_get(search_sids, attributes=attributes, sid_encode=sid_encode)
        yield from generator

    def do_get(
        self,
        search_sids: List[Sid],
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Iterator[Mapping[str, Any]]:
        """
        Has the same purpose as get(), but operates on given "search_sids",
        a list of typed search sids.

        Is called by get() after unfolding and typing the search sid.

        Args:
            search_sids: List of typed search sids.
            attributes: a list of attribute names, that should be fetched.
            sid_encode: a callable to which the sid object will be passed, that should return the value added to the data dictionary under the "sid" key.
                        Example: `sid_encode=lambda x: x.uri`
                        If the callable returns None, the value is not added. As in `sid_encode=lambda x: None`

        Returns:
            Iterator over Mappings containing the retrieved data.
            One special field named "sid" contains the Sid.
        """
        raise NotImplementedError("Method do_get() needs to be implemented.")

    def get_one(
        self,
        search_sid: str | Sid,
        attributes: Optional[List[str]] = None,
        sid_encode: Callable = str,
    ) -> Mapping[str, Any]:
        """
        Calls get() with the given parameters, and returns the first result.

        Args:
            See get()

        Returns:
            Mapping containing the retrieved data.
            One special field named "sid" contains the Sid
        """
        found = first(self.get(search_sid, attributes=attributes, sid_encode=sid_encode))
        return found or {}

    def get_data(
        self, sid: str | Sid, attributes: Optional[List[str]] = None, sid_encode: Callable = str
    ) -> Mapping[str, Any]:
        """
        Returns data associated to the given Sid, as a key:value dictionary.
        One special field named "sid" contains the Sid.

        Returns an empty dictionary if no data was found.

        Args:
            sid: a typed sid
            attributes: a list of attribute names, that should be fetched.
            sid_encode: a callable to which the sid object will be passed, that should return the value added to the data dictionary under the "sid" key.
                        Example: `sid_encode=lambda x: x.uri`
                        If the callable returns None, the value is not added. As in `sid_encode=lambda x: None`

        Returns:
            Mapping containing the retrieved data.
            One special field named "sid" contains the Sid
        """
        return self.get_one(search_sid=sid, attributes=attributes, sid_encode=sid_encode)

    def get_attr(self, sid: str | Sid, attribute: str) -> Any | None:
        """
        Returns an attribute, a named piece of data, for the given Sid.

        Args:
            sid: typed Sid
            attribute: attribute name

        Returns:
            The value for the given Sid and attribute name.
        """
        return self.get_data(sid).get(attribute)

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


if __name__ == "__main__":
    print(Getter())
