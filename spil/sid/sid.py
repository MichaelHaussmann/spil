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
from typing import Iterable, Any, Optional, Dict

from os import PathLike
import importlib
from functools import total_ordering

from spil.sid.core import uri_helper
from spil.util.caching import lru_cache as cache
from spil.util.log import debug, info, warning

from spil import conf
from spil.util.exception import SpilException


class BaseSid:
    """Base class for Sids.

    Implements __new__ and __init__ to allow Sid instances to be created by a factory.
    The goal is to have an extendable Sid and factory.
    """

    def __new__(cls, *args, **kwargs):
        """
        Calls a Factory function that handles the Sid object creation.
        Returns the instance from that factory.

        (To avoid that the factory calls itself,
        the method uses the kwarg "from_factory".
        If it is set, an object instance is returned.)

        Args:
            *args:
            **kwargs:
        """
        if not kwargs.get("from_factory"):
            (mod, fn) = cls._factory
            mod = importlib.import_module(mod)
            fn = getattr(mod, fn)
            return fn(*args, **kwargs)
        else:
            return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        """
        Empty Method.
        See documentation about the Sid Factory creation mechanism.

        Args:
            *args:
            **kwargs:
        """
        pass


@total_ordering
class StringSid(BaseSid):
    """
    StringSid is the barest type of Sids.

    It only has a string.
    It is not typed.
    """
    _string = ''

    @property
    def string(self) -> str:
        """
        Returns the string representation of a Sid.
        The string can be any arbitrary string if the Sid is not typed.

        If the Sid is typed, the string will is a path like representation of its values.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0100/anim').string
            "hamlet/s/sq030/sh0100/anim"

            >>> Sid('blablabla').string
            "blablabla"

        Returns:
            The string representation.
        """
        return self._string

    @property
    def full_string(self) -> str:
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        Returns: The long string representation.

        """
        return self._string

    def copy(self) -> Sid:
        """
        Returns a copy of the current Sid.
        Copy is generated by calling `Sid(self.full_string)`.

        Example:

            >>> Sid('hamlet/a/char/romeo/modeling')
            Sid('hamlet/a/char/romeo/modeling')

        Returns:
            A Sid copy.

        """
        return Sid(self.full_string)  # self.get_with()

    def is_search(self) -> bool:
        """
        Returns True if the current Sid contains search symbols.
        Search symbols are defined in the Sid conf, and are typically: ['*', ',', '>', '<', '**']

        The Sid may not be typed.

        Examples:
            >>> Sid('hamlet/a/char/*/*')
            True

        Returns:
            True if the Sid contains search symbols, else False.

        """
        return any(s in str(self) for s in conf.search_symbols)

    def __str__(self) -> str:
        return self._string

    def __repr__(self) -> str:
        return 'Sid("{0}")'.format(self.full_string)

    def __hash__(self, *args, **kwargs) -> int:
        return hash(repr(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sid):
            return str(other.full_string) == str(self.full_string)
        else:
            return str(other) == str(self)

    def __lt__(self, other: Sid | str) -> bool:
        return str(self) < str(other)

    def __truediv__(self, other: Sid | str) -> Sid:
        """
        Override the division operator, to compose a Sid from another one.
        Inspired by pathlib.Path.

        Examples:

            >>> Sid('hamlet') / 's' / 'sq030'
            "hamlet/s/sq030"

            >>> sid.parent / sid.get(sid.keytype) == sid
        """
        return Sid(str(self) + conf.sip + str(other))


class TypedSid(StringSid):

    def _init(self, string: Optional[str] = None, type: Optional[str] = None, fields: Optional[dict] = None):
        # print(f"DataSid._init {string}, {type}, {fields}")
        self._string = string or ''
        self._type = type or ''
        self._fields = fields or dict()

    @property
    def type(self) -> str:
        return self._type

    @property
    def fields(self) -> dict:
        return self._fields.copy()

    @property
    def full_string(self) -> str:
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0100/anim').full_string
            "shot__task:hamlet/s/sq030/sh0100/anim"

            >>> Sid('blablabla').full_string
            "blablabla"
        """
        return '{}{}'.format(self._type + ':' if self._type else '', self.string)

    @property
    def basetype(self) -> str | None:
        """
        The basetype is the first part of the type.
        Example:
            for type "shot__file"  -> basetype = "shot"

        Example:

            >>> Sid('hamlet/s/sq030/sh0100/anim').basetype
            "shot"

        Returns
            string basetype
        """
        # raise PendingDeprecationWarning("basetype may be deprecated in the future")

        result = None
        if not self._type:
            info('This Sid has no type. ({})'.format(self))
            return None
        try:
            result = self._type.split(conf.sidtype_keytype_sep)[0]
        except Exception as e:
            info('[sid][basetype] Unable to get basetype. Sid: {} ("{}")'.format(self, e))
        return result

    @property
    def keytype(self) -> str | None:
        """
        Returns the last key of the fields dictionary.

        Note that this is not necessarily the second part of the "type".

        Examples:
        Sid("hamlet/a/char/claudius/model/v001/w/blend")
        type: 'asset__file'
        keytype: 'ext'
        basetype: 'asset'

        Sid("hamlet/s")
        type: 'shot'
        keytype: 'type'
        basetype: 'shot'

        Sid("hamlet")
        type: 'project'
        keytype: 'project'
        basetype: 'project'

        Examples:
        >>>Sid('hamlet/a/char/romeo/model').keytype
        "task"

        >>>Sid('hamlet/s/sq001/sh0010').keytype
        "shot"

        :return: string keytype
        """
        if not self._fields:
            warning('[Sid][keytype] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return None
        return list(self._fields.keys() or [None])[-1]

    @property
    def parent(self) -> Sid:
        """
        Returns the parent Sid.

        If the
        Returns an empty Sid, if the Sid is not "defined", or self if the Sid is already the root (has no parent).

        Example:
        >>> Sid('hamlet/s/sq030/sh0100').parent
        Sid('hamlet/s/sq030')
        """
        if not self._fields:
            warning('[Sid][parent] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()
        if len(self._fields.keys()) == 1:
            return self.copy()
        parent_key = list(self._fields.keys())[-2]
        return self.get_as(parent_key)

    def __len__(self) -> int:
        return len(self._fields)

    def get(self, key: str) -> str | None:
        """
        Returns the value of given key.
        As defined in the internal "fields" dictionary.

        Example:
        >>> Sid('hamlet/s/sq030/sh0100/anim').get('shot')
        "sh0100"
        """

        if not self._fields:
            warning('[Sid][get] Asked for a Sid operation on an undefined Sid: "{}"'.format(self.string))
            return None

        return self._fields.get(key)

    def get_as(self, key: str) -> Sid:
        """
        Returns a new Sid built of the fields until (and including) the given key.

        Example:
        >>> Sid('hamlet/a/char/romeo/model/v001/w/ma').get_as('task')
        Sid('hamlet/a/char/romeo/model')
        """

        if not self._fields:
            warning('[Sid][get_as] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()  # Return type is always Sid.

        if key not in self._fields:
            info(f'[Sid][get_as] Key "{key}" not found in fields "{self._fields}"')
            return Sid()

        fields = dict()
        for k, v in self._fields.items():
            fields[k] = v
            if k == key:
                return Sid(fields=fields)

        raise SpilException(f"[Sid][get_as] Something unexpected happened during {self}.get_as({key})")

    def get_with(self,
                 uri: Optional[str] = None,
                 key: Optional[str] = None,
                 value: Optional[str] = None,
                 **kwargs) -> Sid:
        """
        Returns a new Sid with
        - the given uri applied (see details in documentation)
        or
        - updated using given key and value, eg get_with(key='task', value='rendering') and
        - updated using **kwargs where keys are sid keys, eg get_with(task='rendering')

        Depending on the update, the type of the returned Sid can change.

        A key set to None will be removed.
        To empty a keys value, set it to an empty string "".

        Examples:
        >>> Sid('hamlet/s/sq030/sh0010/animation').get_with(task='rendering')
        Sid('hamlet/s/sq030/sh0010/rendering')

        >>> Sid("hamlet/a/props/dagger").get_with(uri='asset=skull')
        Sid('hamlet/a/props/skull')

        :param uri: a uri string
        :param key: a key name
        :param value: a value for attribute
        :param kwargs: a key/value dictionary
        :return:
        """
        if not self._fields:
            warning(f'[Sid][get_with] Asked for a Sid operation on an undefined Sid "{self.string}"')
            return Sid()  # Return type is always Sid.

        # if we have a uri
        if uri:
            return Sid('{}?{}'.format(self.full_string, uri))

        data_copy = self._fields.copy()

        if key:
            kwargs[key] = value
        for key, value in kwargs.copy().items():  # removing a key if the value is None. Use '' for empty values.
            if value is None:
                data_copy.pop(key)
                kwargs.pop(key)

        data_copy.update(kwargs)
        new_sid = Sid(fields=data_copy)
        # If the resulting Sid is not typed, we try return as StringSid, matching the Sid dictionary.
        # This is useful for search Sids.
        if not new_sid:
            new_sid = Sid('/'.join(list(data_copy.values())))
        return new_sid

    def is_leaf(self):
        """
        Returns True if the current Sid is a leaf node.

        Current implementation checks if the keytype is set as a leaf type in the config_name.
        For example: "ext" (file extension) is the keytype of leaf nodes.
        This is configured per basetype.

        This method is experimental. Implementation and concept to be clarified.

        Note: A leaf should be dependent on the context and type.
        For example, in searching for render files,
        it can be useful to handle the "render pass" as leave,
        to avoid going too deep in the hierarchy.
        This is done in the browser, to browse render files by the pass folder, not individually by default.

        :return: bool
        """
        return bool(self.get(conf.leaf_keys.get(self.basetype)))
        # TODO:
        # Better define "complete". Also in regard to a search Sid. For example Sids containing /** are "complete".
        # or if a Sid has no children, it is leaf.

    def as_uri(self) -> str:
        """
        Returns the fields as a key value string, as in an URI.


        Example:
        >>>Sid('hamlet/a/char/ophelia/model').as_uri()
        "project=hamlet&type=a&cat=char&name=ophelia&task=model"

        :return: string uri
        """
        return uri_helper.to_string(self._fields)

    def match(self, search_sid: Sid | str) -> bool:  # IDEA: match_as(search_sid, key) for example, do the "seq" of both sids match (like is_relative_to ?)
        """
        Returns True if a given search_sid matches the current Sid.
        Else False.

        This method is useful to create filters matching groups of Sids, more precise than types.

        Example:
        >>>Sid('hamlet/a/char/romeo/model').match('hamlet/a/*/*/model')
        True
        >>>Sid('hamlet/s/sq030/sh0100/anim').match('hamlet/s/*/*/*')
        True
        >>>Sid('hamlet/a/char/romeo').match('hamlet/a/prop/*')
        False

        :return: bool
        """
        # Identicals always match
        if Sid(search_sid) == self:
            return True
        if not self._fields:  # Should untyped sids be able to match ? Identical strings could match.
            warning('[Sid][match] Asked for a match check on an undefined Sid: "{}". Returning False.'.format(self.string))
            return False
        # To check the match, we search in a list with self as single element,
        # and expect self to be found using given search_sid.
        from spil import FindInList
        fl = FindInList([self.string])
        return fl.find_one(search_sid, as_sid=False) == self.string


class PathSid(TypedSid):

    @cache
    def path(self, config: Optional[str] = None) -> Pathlike[str]:  # type: ignore
        """
        Returns the file path for the current Sid, as a pathlib.Path.
        Returns None if the Sid has no path, or if it cannot be resolved.

        Example:
            >>> Sid('hamlet/a/char/romeo/model/v001/w/ma').path()
            Path("/productions/hamlet/assets/characters/romeo/3d/modeling/works/romeo_v001.ma")

        Args:
            config: Name of the path config to be used, as configured.

        Returns:
            A path, if the Sid has a path, else None.
        """
        from spil.sid.pathops.fs_resolver import dict_to_path
        result = None
        try:
            result = dict_to_path(self._fields, self._type, config=config)
        except SpilException as e:
            debug(f"This Sid has no path (config_name: {config}). ({e})")
        return result


class DataSid(PathSid):

    # TODO: make configurable which Finder is used for DataSid operations (FindInFinders per default).
    # Could be handled using a default config_name, and/or be changed at runtime.

    def get_last(self, key: Optional[str] = None) -> Sid:
        """
        Returns a new Sid object, with the same fields as self, and the last existing match for given key.
        If key is not given, the keytype is used.

        Examples:
            >>>Sid('hamlet/a/char/romeo/model/v001/w/ma').get_last('version')
            Sid('hamlet/a/char/romeo/model/v008/w/ma')

            >>>Sid('hamlet/a/char/romeo/model').get_last()
            Sid('hamlet/a/char/romeo/shading')

        This method calls Finder internally, and is a shortcut to:
            Finder().find_one(self.get_with(key=key, value='>'), as_sid=True)

        Note: Sid sorting is currently limited to string values, which usually works with versions.
        A meaningful sorting (eg. "render" after "animation") is planned.

        (implementation is experimental)

        :return: Sid
        """
        if not key:
            key = self.keytype
        from spil import FindInFinders
        found = FindInFinders().find_one(self.get_with(key=key, value='>'), as_sid=True)
        if found.get(key):  # little failsafe. #SMELL
            return found
        else:
            return Sid()

    def get_attr(self, attribute: str) -> Any | None:
        """
        Returns an attribute for the current sid as defined in data_conf.

        Shortcut to data.find(sid, attribute), which is called internally.

        Example:
        >>> Sid('hamlet/a/char/romeo/model/v001/w/ma').get_attr('comment')
        "first version"
        """
        from spil.data.data import get  # FIXME: WIP
        value = get(self, attribute)
        if value:
            return value
        else:
            return None

    def get_next(self, key):  # FIXME: delegate to Data framework
        """
        This method is experimental. Do not use.

        Returns self with version incremented, or first version if there is no version.
        If version is '*', returns "new" version (next of last)

        If the result is not a valid Sid (not typed, no fields), returns an empty Sid.

        :return: Sid
        """
        if key != 'version':
            raise NotImplementedError("get_next() support only 'version' key for the moment.")
        current = self.get('version')
        if current:
            if current in ['*', '>']:  #FIXME: point to "searcher signs" config_name
                version = (self.get_last('version').get('version') or 'v000').split('v')[-1] or 0
            else:
                version = self.get('version').split('v')[-1]  # temporary workaround for "v001" FIXME
        else:
            version = 0  # allow non existing version #RULE: starts with V001 (#FIXME)
        version = (int(version) + 1)
        version = 'v' + str('%03d' % version)
        result = self.get_with(version=version)
        return result if result else Sid()

    def get_new(self, key):  # FIXME: delegate to Data framework
        """
        This implementation is experimental.

        Returns self with next of last version, or first version if there is no version.

        If the result is not a valid Sid (not typed, no fields), returns an empty Sid.

        :return: Sid
        """
        if key != 'version':
            raise NotImplementedError("get_new() support only 'version' key for the moment.")
        if self.get('version'):
            if self.get_last('version'):
                result = self.get_last('version').get_next('version')
                return result if result else Sid()
            else:
                result = self.get_next('version')  # Returns a first version
                return result if result else Sid()
        else:
            with_added_version = self.get_with(version='*').get_last('version')
            if with_added_version:
                result = with_added_version.get_next('version')
                return result if result else Sid()
            else:
                result = self.get_next('version')  # Returns a first version
                return result if result else Sid()

    def exists(self) -> bool:
        """
        Returns True if the current Sid exists.
        Shortcut to Finder().exists(sid), which is called internally.

        :return: bool
        """
        from spil import FindInFinders
        return FindInFinders().exists(self)

    def siblings_as(self, key: str) -> Iterable[Sid]:
        if key not in self._fields:
            info(f'[Sid][siblings_as] Key "{key}" not found in fields "{self._fields}"')
            return []
        search = self.get_as(key).get_with(key=key, value='*')
        from spil import FindInFinders as FT
        for i in FT().find(search, as_sid=True):
            yield i

    def siblings(self) -> Iterable[Sid]:
        return self.siblings_as(self.keytype)

    def children(self) -> Iterable[Sid]:
        if self.is_leaf():  # per definition, leafs have no children.
            return []
        from spil import FindInFinders as FT
        search = self / '*'
        for i in FT().find(search, as_sid=True):
            yield i

    # def get_first, get_next, get_previous, get_parent, get_children, project / thing / thing
    # implement URIs: Sid('FTOT').get_with(uri='type=A') <==> FTOT?type=A  ==>  FTOT/A
    # define "complete / incomplete" sid.is_leaf ? (root / anchor / parent / parents /
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent


class Sid(DataSid):
    """
    Sid class.
    """

    _factory = ('spil.sid.core.sid_factory', 'sid_factory')  # TODO: config_name, or better system.


if __name__ == '__main__':

    from spil_tests import stop
    from pprint import pprint
    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(INFO)

    s = Sid("hamlet/s/sq010/sh0010/anim")
    print(s.exists())
    print(list(s.children()))
