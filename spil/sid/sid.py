"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
from typing import Any, Optional, List

import importlib
from functools import total_ordering
from pathlib import Path

from spil.sid.core import query_helper
from spil.util.caching import lru_cache as cache
from spil.util.log import debug, info, warning

from spil import conf
from spil.util.exception import SpilException

"""
TODO:

Notes.
We need a STRICT mode, where type changes are warned, or changes to untyped are errored.
Example:
an erroneous usage of get_with() can silently change the Sid type to an unexpected one, 
or loose the type, and the error goes undetected.
We could use a target type for Sids operations.
We could use a global data validation framework (pydantic, apischema or so).
"""


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
    StringSid is the barest form of Sids.
    It only has a string.
    It is not typed.
    """

    _string = ""

    @property
    def string(self) -> str:
        """
        Returns the string representation of a Sid.
        The string can be any arbitrary string if the Sid is not typed.

        If the Sid is typed, the string will is a path like representation of its values.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0100/anim').string
            'hamlet/s/sq030/sh0100/anim'

            >>> Sid('blablabla').string
            'blablabla'

        Returns:
            The string representation.
        """
        return self._string

    @property
    def full_string(self) -> str:
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        (This property is overriden in TypedSid)

        Returns:
            The long string representation.
        """
        return self._string

    def copy(self) -> Sid:
        """
        Returns a copy of the current Sid.
        Copy is generated by calling `Sid(self.full_string)`.

        Example:

            >>> Sid('hamlet/a/char/ophelia/model').copy()
            Sid('asset__task:hamlet/a/char/ophelia/model')

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

            >>> Sid('hamlet/a/char/*/*').is_search()
            True

            >>> Sid('hamlet/a/char/ophelia').is_search()
            False

        Returns:
            True if the Sid contains search symbols, else False.

        """
        return any(s in str(self) for s in conf.search_symbols)

    def __str__(self) -> str:
        return self._string

    def __repr__(self) -> str:
        return "Sid('{0}')".format(self.full_string)

    def __hash__(self, *args, **kwargs) -> int:
        return hash(repr(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sid):
            return str(other.full_string) == str(self.full_string)
        else:
            return str(other) == str(self)

    def __lt__(self, other: Sid | str) -> bool:
        return str(self) < str(other)

    def __truediv__(self, other: Sid | str | None) -> Sid:
        """
        Override the division operator, to compose a Sid from another one.
        Inspired by pathlib.Path.

        The get_with() method is prefered, since it generally is less "volatile".

        Examples:

            >>> Sid('hamlet') / 's' / 'sq030'
            Sid('shot__sequence:hamlet/s/sq030')

            >>> sid = Sid("hamlet/s/sq030")
            >>> sid.parent / sid.get(sid.keytype) == sid
            True

            >>> Sid("hamlet/s/sq030") / None
            Sid('shot__sequence:hamlet/s/sq030')
        """
        if other is None:
            return self.copy()
        return Sid(str(self) + conf.sip + str(other))


class TypedSid(StringSid):
    """
    The TypedSid class implements a Sid that has been resolved successfully.
    It has a "type" and a "field" data dictionary.
    """

    def _init(
        self,
        string: Optional[str] = None,
        type: Optional[str] = None,
        fields: Optional[dict] = None,
    ):
        self._string = string or ""
        self._type = type or ""
        self._fields = fields or {}

    @property
    def type(self) -> str:
        """
        Returns the Sids type.
        If the Sid has no type, an empty string is returned.

        Examples:

            >>> Sid("hamlet/a/char/ophelia/rig").type
            'asset__task'

            >>> Sid("hamlet/a/char/*").type
            'asset__asset'

            >>> Sid("blabla").type
            ''

        Returns:
            The Sid type
        """
        return self._type

    @property
    def fields(self) -> dict:
        """
        Returns the Sids data dictionary.
        The fields match what is defined in the Sid template.

        >>> Sid("hamlet/a/char/*").fields
        OrderedDict([('project', 'hamlet'), ('type', 'a'), ('assettype', 'char'), ('asset', '*')])

        >>> Sid("hamlet/s/sq010/sh0010/anim").fields
        OrderedDict([('project', 'hamlet'), ('type', 's'), ('sequence', 'sq010'), ('shot', 'sh0010'), ('task', 'anim')])

        Returns:
            Sids data dictionary.
        """
        return self._fields.copy()

    @property
    def full_string(self) -> str:
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0100/anim').full_string
            'shot__task:hamlet/s/sq030/sh0100/anim'

            >>> Sid('blablabla').full_string
            'blablabla'

        Returns
            the long string representation of a Sid.
        """
        return "{}{}".format(self._type + ":" if self._type else "", self.string)

    @property
    def basetype(self) -> str | None:
        """
        The basetype is the first part of the type.

        Examples:

            >>> Sid("hamlet/s/sq030/sh0100/anim").basetype
            'shot'

            >>> Sid("hamlet/a/prop/dagger").basetype
            'asset'

            >>> Sid("bla/bla").basetype


        Returns
            string basetype
        """
        result = None
        if not self._type:
            info(f"This Sid has no type. ({self})")
            return None
        try:
            result = self._type.split(conf.sidtype_keytype_sep)[0]
        except Exception as e:
            info(f'[sid][basetype] Unable to get basetype. Sid: {self} ("{e}")')
        return result

    @property
    def keytype(self) -> str | None:
        """
        Returns the last key of the fields dictionary.

        Note that this is not necessarily the second part of the "type".

        ```
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
        ```

        Examples:

            >>> Sid("hamlet/a/char/claudius/model/v001/w/blend").keytype
            'ext'

            >>> Sid("hamlet/a/char/ophelia/model").keytype
            'task'

            >>> Sid("hamlet/s/sq001/sh0010").keytype
            'shot'

        Returns:
             string keytype
        """
        if not self._fields:
            warning(f'Sid operation on an undefined Sid "{self.string}"')
            return None
        return list(self._fields.keys() or [None])[-1]

    @property
    def parent(self) -> Sid:
        """
        Returns the parent Sid.
        Returns an empty Sid, if the Sid is not "defined", or a copy of self if the Sid is already the root (has no parent).

        Note that this is a logical operation, without data access.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0100').parent
            Sid('shot__sequence:hamlet/s/sq030')

            >>> Sid('hamlet').parent
            Sid('project:hamlet')

            >>> Sid('bla/bla/bla').parent
            Sid('')

        Returns:
            Returns an empty Sid, if the Sid is not "defined", or self if the Sid is already the root (has no parent).

        """
        if not self._fields:
            warning(f'Sid operation on an undefined Sid "{self.string}"')
            return Sid()
        if len(self._fields.keys()) == 1:
            return self.copy()
        parent_key = list(self._fields.keys())[-2]
        return self.get_as(parent_key)

    def __len__(self) -> int:
        """
        Returns the "length" of a Sid, which is the number of keys in its "fields" data dictionary.

        Returns:
            The amount of keys in the "fields" dictionary.
        """
        return len(self._fields)

    def get(self, key: str) -> str | None:
        """
        Returns the value of given key.
        As defined in the internal "fields" data dictionary.

        Example:

            >>> Sid("hamlet/s/sq030/sh0100/anim").get("shot")
            'sh0100'

        Args:
            key: retrieved key

        Returns:
            Value of given key, in the "fields" data dictionary.

        """
        if not self._fields:
            warning(f'Sid operation on an undefined Sid "{self.string}"')
            return None

        return self._fields.get(key)

    def get_as(self, key: str) -> Sid:
        """
        Returns a new Sid built of the fields until (and including) the given key.
        If the Sid is not typed or the key is not found, an empty Sid is returned.

        Example:

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_as('task')
            Sid('asset__task:hamlet/a/char/ophelia/model')

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_as('something')
            Sid('')

            >>> Sid('hamlet/bla/bla').get_as('shot')
            Sid('')

        Args:
            key: key until which the new Sid should be built

        Returns:
            Sid as given key

        """
        if not self._fields:
            warning(f'Sid operation on an undefined Sid "{self.string}"')
            return Sid()  # Return type is always Sid.

        if key not in self._fields:
            info(f'Key "{key}" not found in fields "{self._fields}"')
            return Sid()

        fields = {}
        for k, v in self._fields.items():
            fields[k] = v
            if k == key:
                return Sid(fields=fields)

        raise SpilException(f"[Sid][get_as] Unexpected error during {self}.get_as({key})")

    def get_with(
        self,
        query: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs,
    ) -> Sid:
        """
        Returns a new Sid
        - with the given query applied (see details about query application in documentation)
        or
        - updated using given key and value, eg. get_with(key='task', value='rendering') and
        - updated using **kwargs where keys are sid keys, eg. get_with(task='rendering')

        Depending on the update, the type of the returned Sid can change, or the Sid can end up untyped.

        A key set to None will be removed.
        To empty a keys value, set it to an empty string "".

        Note: only works on typed or empty Sids.

        Examples:

            >>> Sid('hamlet/s/sq030/sh0010/anim').get_with(task='render')
            Sid('shot__task:hamlet/s/sq030/sh0010/render')

            >>> Sid("hamlet/a/prop/dagger").get_with(query='asset=skull')
            Sid('asset__asset:hamlet/a/prop/skull')

            >>> Sid().get_with(project="hamlet")
            Sid('project:hamlet')

        Args:
            query: s tring query, in the format ?key=value&key2=value2
            key: a key name, for example "shot", "sequence", or "task"
            value: a new value for given key. May be None (removes the key) or "" (empty value).
            **kwargs: a key/value dictionary

        Returns:
            A new Sid. Depending on the update, the type of the returned Sid can change.
        """
        if self._string and not self._fields:
            warning(f'Sid operation on an undefined Sid "{self.string}"')
            return Sid()  # Return type is always Sid.

        # if we have a query
        if query:
            return Sid("{}?{}".format(self.full_string, query))

        data_copy = self._fields.copy()

        if key:
            kwargs[key] = value

        for key, value in kwargs.copy().items():
            # removing a key if the value is None. Use '' for empty values.
            if value is None:
                data_copy.pop(key)
                kwargs.pop(key)

        data_copy.update(kwargs)
        new_sid = Sid(fields=data_copy)
        # If the resulting Sid is not typed, and is a search, we try return as StringSid, matching the Sid dictionary.
        # This is useful but may have unexpected side effects.
        if new_sid.is_search() and not new_sid:
            new_sid = Sid("/".join(list(data_copy.values())))
        return new_sid

    def is_leaf(self):
        """
        Returns True if the current Sid is a "leaf" node.
        A leaf node has no children (and cannot have children).

        Current implementation checks if the keytype is set as a "leaf type" in the config_name.
        For example: "ext" (file extension) is the keytype of leaf nodes.
        This is configured per basetype.

        This implementation is still experimental.
        Implementation and concept needs to be clarified.

        Note: A leaf should be dependent on the context and type.
        For example, in searching for render files,
        it can be useful to handle the "render pass" as leave,
        to avoid going too deep in the hierarchy.

        This is done, for example, in the spil_ui browser,
        to browse render files by the pass folder,
        not individually by default.

        Returns:
            True if this Sid is a leaf, else False.
        """
        return bool(self.get(conf.leaf_keys.get(self.basetype)))
        # TODO:
        # Better define "complete". Also in regard to a search Sid.
        # For example Sids containing /** are "complete".
        # or if a Sid has no children, it is leaf.

    def as_query(self) -> str:
        """
        Returns the fields as a key value string, as in an Query.

        Example:

            >>> Sid('hamlet/a/char/ophelia/model').as_query()
            'project=hamlet&type=a&assettype=char&asset=ophelia&task=model'

        Returns:
            string query

        """
        return query_helper.to_string(self._fields)

    # IDEA: match_as(search_sid, key) for example, do the "seq" of both sids match (like is_relative_to ?)
    def match(self, search_sid: Sid | str) -> bool:
        """
        Returns True if a given search_sid matches the current Sid.
        Else False.

        This method is useful to create filters matching groups of Sids, more precise than types.

        Examples:

            >>> Sid('hamlet/a/char/ophelia/model').match('hamlet/a/*/*/model')
            True

            >>> Sid('hamlet/s/sq030/sh0100/anim').match('hamlet/s/*/*/*')
            True

            >>> Sid('hamlet/a/char/ophelia').match('hamlet/a/prop/*')
            False

        Returns
            True if matched, else False
        """
        # Identicals always match
        if Sid(search_sid) == self:
            return True
        # Should untyped sids be able to match ? Identical strings could match.
        if not self._fields:
            warning(f'Cannot match check an undefined Sid: "{self.string}". Returning False.')
            return False
        # To check the match, we search in a list with self as single element,
        # and expect self to be found using given search_sid.
        from spil import FindInList  # fmt: skip
        fl = FindInList([self.string])
        return fl.find_one(search_sid, as_sid=False) == self.string


class PathSid(TypedSid):
    """
    The PathSid adds path resolving.

    TODO: cache must be invalidated whenever (if ever) the default PathConfig changes.
    """

    @cache
    def path(self, config: Optional[str] = None) -> Path | None:
        """
        Returns the file path for the current Sid, as a pathlib.Path.
        Returns None if the Sid has no path, or if it cannot be resolved.

        This method is cached.
        A path for a Sid is configured (not the result of a data lookup),
        and is not supposed to change during runtime.

        Example:

            >>> sid = Sid('hamlet/a/char/ophelia/model/v001/w/ma')
            >>> path = sid.path()
            >>> new_sid = Sid(path=path)
            >>> sid == new_sid
            True

            >>> path = Sid('hamlet/a/char/ophelia/model/v001/w/ma').path()
            >>> path.relative_to(conf.default_sid_conf_path).as_posix()  # to be location and os independent
            'data/testing/SPIL_PROJECTS/LOCAL/PROJECTS/HAMLET/PROD/ASSETS/char/ophelia/model/v001/char_ophelia_model_WORK_v001.ma'

            >>> Sid('bla/bla').path()

        Args:
            config: Name of the path config to be used, as configured.

        Returns:
            A path, if the Sid has a path, else None.
        """
        if not self._fields:
            debug(f'Sid is undefined: "{self.string}". Returning None.')
            return None
        from spil.sid.pathops.fs_resolver import dict_to_path  # fmt: skip
        result = None
        try:
            result = dict_to_path(self._fields, self._type, config=config)
        except SpilException as e:
            debug(f"This Sid has no path (config_name: {config}). ({e})")
        return result


class DataSid(PathSid):
    """
    The DataSid implements operations that delegate calls to data sources: Finders and Getters.
    By default FindInAll and GetFromAll are used.

    # TODO: make configurable which Finder is used for DataSid operations (FindInAll per default).
    # Could be handled using a default config_name, and/or be changed at runtime.
    """

    def get_attr(self, attribute: str) -> Any | None:
        """
        Returns an attribute for the current sid.
        Uses GetFromAll, which calls the apropriate Getter defined for this Sid in spil_data_conf.

        Shortcut to GetFromAll().get_attr(sid, attribute), which is called internally.

        Example:

            >>> from spil import WriteToPaths
            >>> sid = Sid('hamlet/a/char/ophelia/model/v001/w/ma')
            >>> __ = WriteToPaths().set(sid, comment="Updated topology")
            >>> sid.get_attr('comment')
            'Updated topology'

        Args:
            attribute: Name of an attribute

        Returns:
            The value of the attribute, or None if it was not found.

        """
        from spil import GetFromAll  # fmt: skip
        return GetFromAll().get_attr(self, attribute)  # type: ignore

    def get_last(self, key: Optional[str] = None) -> Sid:
        """
        Returns a new Sid object, with the same fields as self, and the last existing match for given key.
        If key is not given, the keytype is used.
        If the Sid is untyped, returns an empty Sid.

        Examples:

            >>> Sid('hamlet/a/char/ophelia/model/v001/p/ma').get_last('version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v002/p/ma')

            >>> Sid('hamlet/a/char/ophelia/model').get_last()
            Sid('asset__task:hamlet/a/char/ophelia/surface')

            >>> Sid('bla/bla').get_last('whatever')
            Sid('')

        This method calls FindinAll internally, and is a shortcut to:
            FindInAll().find_one(self.get_with(key=key, value='>'), as_sid=True)

        Note: Sid sorting is currently limited to string values, which usually works with versions.
        A meaningful sorting of tasks (eg. "render" after "animation") is planned.

        (implementation is experimental)

        Returns:
            Sid or None
        """
        if not self._fields:
            debug(f'Sid is undefined: "{self.string}". Returning Emptu Sid..')
            return Sid()
        if not key:
            key = self.keytype
        from spil import FindInAll  # fmt: skip
        found = FindInAll().find_one(self.get_with(key=key, value=">"), as_sid=True)
        if found.get(key):  # little failsafe. #SMELL
            return found
        else:
            return Sid()

    def get_next(self, key: str) -> Sid:
        """
        Returns self with key's value incremented, or first value if there is none.
        If value is '*', returns "get_new" (next of last)

        If the result is not a valid Sid (not typed, no fields), returns an empty Sid.

        Note:
            Currently limited to version.

        Examples:

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_next('version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v002/w/ma')

            >>> Sid('hamlet/a/char/ophelia/model/*/w/ma').get_next('version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v003/w/ma')

            >>> Sid('hamlet/a/char/ophelia/model').get_next('version')
            Sid('asset__version:hamlet/a/char/ophelia/model/v001')

        Args:
            key: the key for which we want to increment the value. Typically a version.

        Returns:
            A Sid with key's value incremented, or an empty Sid.

        """
        if key != "version":
            raise NotImplementedError("get_next() support only 'version' key for the moment.")

        attribute = f"next.{key}"

        from spil import GetFromAll  # fmt: skip
        return GetFromAll().get_attr(self, attribute=attribute)  # type: ignore

    def get_new(self, key: str) -> Sid:  # FIXME: Needs testing and documentation
        """
        Returns a new Sid with the key incremented to the "next available value".
        Makes sense with numerical values, especially with versions.

        For example, if the given key is "version":
        Returns self with next version (the one following the last), or first version if there is no version.
        If the result is not a valid Sid (not typed, no fields), returns an empty Sid.

        Example:

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').get_new('version')
            Sid('asset__file:hamlet/a/char/ophelia/model/v003/w/ma')

        Args:
            key:

        Returns:
            Sid

        """
        if self.get(key):
            if self.get_last(key):
                result = self.get_last(key).get_next(key)
                return result or Sid()
            else:
                result = self.get_next(key)  # Returns a first version
                return result or Sid()
        else:
            with_added_key = self.get_with(key=key, value="*").get_last(key)
            if with_added_key:
                result = with_added_key.get_next(key)
                return result or Sid()
            else:
                result = self.get_next(key)  # Returns a first version
                return result or Sid()

    def exists(self) -> bool:
        """
        Returns True if the current Sid exists.
        Shortcut to FindInAll().exists(self), which is called internally.

        Examples:

            >>> Sid('hamlet/a/char/ophelia').exists()
            True

            >>> Sid('hamlet/a/prop/computer').exists()
            False

            >>> Sid('bla/bla').exists()
            False

        Returns:
            True if Sid exists, else False
        """
        if not self._fields:
            debug(f'Sid is undefined: "{self.string}". Returning False')
            return False
        from spil import FindInAll  # fmt: skip
        return FindInAll().exists(self)  # type: ignore

    def siblings_as(self, key: str) -> List[Sid]:
        """
        Returns existing siblings, in other words children of parent, as Sid of given keytype.

        Example:

            >>> Sid('hamlet/a/fx/blood/surface/v002/p/ma').siblings_as('asset')
            [Sid('asset__asset:hamlet/a/fx/blood'), Sid('asset__asset:hamlet/a/fx/rain'), Sid('asset__asset:hamlet/a/fx/water'), Sid('asset__asset:hamlet/a/fx/mist'), Sid('asset__asset:hamlet/a/fx/thunder')]

        Args:
            key: keytype we want siblings from

        Returns:
            List of sibling Sids

        """
        if key not in self._fields:
            info(f'[Sid][siblings_as] Key "{key}" not found in fields "{self._fields}"')
            return []
        search = self.get_as(key).get_with(key=key, value="*")
        from spil import FindInAll  # fmt: skip
        return list(FindInAll().find(search, as_sid=True))

    def siblings(self) -> List[Sid]:
        """
        Returns existing siblings, in other words children of parent.

        Example:

            >>> Sid('hamlet/a/fx/blood/surface').siblings()
            [Sid('asset__task:hamlet/a/fx/blood/model'), Sid('asset__task:hamlet/a/fx/blood/surface'), Sid('asset__task:hamlet/a/fx/blood/art'), Sid('asset__task:hamlet/a/fx/blood/rig')]

        Returns:
            List of sibling Sids.
        """
        return self.siblings_as(self.keytype)

    def children(self) -> List[Sid]:
        """
        Returns existing children.
        Shortcut to:  `FindInAll().find(self / '*', as_sid=True)`

        Examples:

            >>> Sid('hamlet/a/char/ophelia/rig').children()
            [Sid('asset__version:hamlet/a/char/ophelia/rig/v001'), Sid('asset__version:hamlet/a/char/ophelia/rig/v002')]

            >>> Sid('hamlet/a/char/ophelia/model/v001/w/ma').children()
            []

        Returns:
            Children Sids
        """
        if self.is_leaf():  # per definition, leafs have no children.
            return []
        from spil import FindInAll  # fmt: skip
        search = self / "*"
        return list(FindInAll().find(search, as_sid=True))

    # def get_first, get_previous,
    # define "complete / incomplete" sid.is_leaf ? (root / anchor / parent / parents )


class Sid(DataSid):
    """
    Sid class.

    Multiple ways to create a Sid:
    - Sid string, fullstring, query string (starting with "?"), Sid object, or empty string
    - query string
    - fields dictionary
    - path (with optional config)

    Examples:

        >>> Sid("hamlet/s/sq010")                                   # string
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid(sid="hamlet/s/sq010")                               # parameter + string
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid(Sid("hamlet/s/sq010"))                              # Sid object
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid("shot__sequence:hamlet/s/sq010")                    # fullstring
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid("?project=hamlet&type=s&sequence=sq010")             # empty string with query
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid(query="project=hamlet&type=s&sequence=sq010")          # query
        Sid('shot__sequence:hamlet/s/sq010')

        >>> Sid(fields={'project': 'hamlet', 'sequence': 'sq010', 'type': 's'})  # fields dict
        Sid('shot__sequence:hamlet/s/sq010')

        >>> path = Path(conf.default_sid_conf_path) / "data/testing/SPIL_PROJECTS/LOCAL/PROJECTS/HAMLET/PROD/ASSETS/char/ophelia/model/v001/char_ophelia_model_WORK_v001.ma"
        >>> Sid(path=path)           # path (default config) # TODO: any config
        Sid('asset__file:hamlet/a/char/ophelia/model/v001/w/ma')

        >>> Sid(path=path, config='local')   # path (config "local")
        Sid('asset__file:hamlet/a/char/ophelia/model/v001/w/ma')

    This class inherits all functionality from the class hierarchy.
    It only defines the factory to be used to create the Sid.
    Note that this implementation may change, but API will remain the same.
    """

    _factory = ("spil.sid.core.sid_factory", "sid_factory")  # TODO: config_name, or better system.


if __name__ == "__main__":

    from spil_tests import stop
    from pprint import pprint
    from spil.util.log import debug, setLevel, INFO, DEBUG, info

    setLevel(INFO)

    s = Sid("hamlet/s/sq010/sh0010/anim")
    print(s.exists())
    print(list(s.children()))
