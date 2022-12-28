# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from __future__ import annotations
from typing import Iterator, Mapping, Any, List, Optional

from spil import Sid
from spil import conf
from spil.sid.read.util import first
from spil.util.caching import lru_cache as cache

from spil.util.log import debug, info, warning, error


class Getter:
    """
    Interface for Sid Getter.

    Implements common public Sid Search methods "get" and "get_one".
    """

    def __init__(self):
        pass

    def get(self, search_sid: str | Sid, attribute: Optional[str] = None, as_sid: bool = False) -> Iterator[Mapping[str | Sid, Any | dict]]:
        """
        For a given search, returns an Iterator over Mappings containing a Sid as key,
        and the retrieved data as value.

        By default, attribute is None, retrieved data is a dictionary containing all configured data for the Sid type.
        If attribute is given, data contains only the value of the given attribute.

        The Sids returned by Getter.get() should be identical to those returned by Finder.find().
        Getter retrieves data related to these Sids, whereas the Finder only the existing Sids themselves.

        Args:
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

    def __str__(self):
        return f"[spil.{self.__class__.__name__}]"


'''
Drafts from previous implementation

def get(sid, attribute, do_cached=True):  # TODO: put the choice of caching or not in the data source config_name.
    if do_cached:
        return get_cached_attribute(sid, attribute)
    else:
        return get_attribute(sid, attribute)

def get_attribute_source(sid, attribute):
    """
    For a given Sid and attribute, looks up the matching data_source, as given by config_name.
    Return value is a callable (typically a function).
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        error('Sid could not be created, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = conf.get_attribute_source(_sid, attribute)
    if source:
        debug('Getting attribute source for "{} / {}": -> {}'.format(sid, attribute, source))
        return source
    else:
        warning('Attribute Source not found for Sid "{} / {}" ({})'.format(sid, attribute, _sid.type))
        return None


def get_attribute(sid, attribute):
    source = get_attribute_source(sid, attribute)
    if source:
        return source(sid)


@cache
def get_cached_attribute(sid, attribute):
    source = conf.get_attribute_source(sid, attribute)
    if source:
        return source(sid)


def reload_data_source(sid):
    """
    Reloads the data source for given sid
    """
'''

if __name__ == "__main__":
    print(Getter())
    