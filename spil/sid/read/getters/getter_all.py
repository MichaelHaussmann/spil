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

    def get_next(self, search_sid: str | Sid, key: str) -> Sid:  # FIXME: delegate to Data framework
        """
        Note: This method is experimental and may be moved.
        It needs to be implemented by the user depending on configuration.

        Lets start with some definitions.

        For a Sid, we can ask for "last", "next" and "new" for a given key.

        Example:
            Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_last('version')
        would return
            Sid('asset__file:hamlet/a/char/ophelia/model/v005/w/ma')
        given that there v005 is the last existing version matching with the current Sid.

        This works also on "search sids" (with "*" in it), and for non numerical, sorted keys

        Example:
            Sid('hamlet/a/char/*').get_last('asset')
        would return:
            Sid('asset__asset:hamlet/a/char/polonius')
        Because "Polonius" is the last existing character.

        Note:
            Currently, values are sorted as strings, which makes sense for certain keys.
            "Tasks" are not yet sorted in a way that would make sense in a pipeline (eg. layout < animation < render)

        Under the hood, this works by updating the Sid and quering a Finder.

        Example:
            Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_last('version')
        becomes this search:
            'hamlet/a/char/ophelia/model/>/w/ma'
        Where ">" means "last.

        Now, clarification on "last", "next" and "new".

        - "last" is the last existing value.
        For example, for 'hamlet/s/sq010/sh0020' and key "shot",
        would look up the last matching shot for sequence sq010, eg
        'hamlet/s/sq010/>'

        - "next" is the value following the current one, "current += 1".
        For example, for 'hamlet/a/char/ophelia/model/v001/w/ma' and key "version"
        the next version is 'hamlet/a/char/ophelia/model/v002/w/ma'
        This is a "theoretical" operation.
        The implementation depends on the key - how do we count up any given key.
        For this reason, this operation is delegated to a configurable function outside spil.

        - "new" is the "next" from the "last".
        This is useful, for example, to get the next available version number.
        If no "last" exists, returns the first value.

        Note: The result is valid the moment it is returned, but is not safe in case of concurrent calls.
        (for example if another process creates a version after the result was returned).
        To prevent conflicts, either the "new" mechanism is implemented at a lower level (database for example),
        or a transaction mechanism is implemented otherwise (try / rollback or commit).


        Returns self with "key"'s value incremented, or first value if no Sid with any value exists.
        If value is '*', returns "new" value (next of last)



        If the result is not a valid Sid (not typed, no fields), returns an empty Sid.

        Example:

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_next('version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v002/w/ma')

        Args:
            key:

        Returns:
            Sid
        """
        raise NotImplementedError("This method needs re-implementation")  # type: ignore

        if key != "version":
            raise NotImplementedError("get_next() support only 'version' key for the moment.")
        current = self.get("version")
        if current:
            if current in ["*", ">"]:  # FIXME: point to "searcher signs" config_name
                version = (self.get_last("version").get("version") or "v000").split("v")[-1] or 0
            else:
                version = self.get("version").split("v")[
                    -1
                ]  # temporary workaround for "v001" FIXME
        else:
            version = 0  # allow non existing version #RULE: starts with V001 (#FIXME)
        version = int(version) + 1
        version = "v" + str("%03d" % version)
        result = self.get_with(version=version)
        return result or Sid()


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
    