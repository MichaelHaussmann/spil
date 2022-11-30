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

import os
from functools import total_ordering

from spil.sid.core import uri_helper
from spil.util.log import warning, debug

from spil import conf
from spil.util.exception import SpilException

import importlib


class Sid:

    _factory = ('spil.sid.core.sid_factory', 'sid_factory')  # TODO: config, or better system.

    def __new__(cls, *args, **kwargs):
        if cls == Sid:
            (mod, fn) = cls._factory
            mod = importlib.import_module(mod)
            fn = getattr(mod, fn)
            return fn(*args, **kwargs)
        else:
            return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        pass


@total_ordering
class DataSid(Sid):
    """
    A Sid is first and foremost:
    An immutable string, looking like a path, and representing hierarchical data.

    Examples:
        (for a movie called Romeo & Juliette, "roju")
         'roju/s/sq0030/sh0100/animation'
         'roju/s/sq0030/sh0100/rendering'
         'roju/s/sq0030/sh0100'
         'roju/a/chars/romeo/modeling/v001/w/ma'
         'roju/a/chars'
         'roju'

    At Sid creation time, the string is "resolved", matched against a config.
    This defines its internal type, and store its data in a dictionary.

    Finally, a Sid contains 3 values.

    1) A string
    This is the bare minimum for a Sid to exist. By default it is an empty string.

    2) A data dictionary
    If the string matches a defined pattern, the data dictionary is filled.
    It is a Defined Sid / a resolved Sid.

    3) A type
    The matching pattern gives the Sid its type.
    The type is of form basetype__keytype.
    If the Sid contains meta-characters (eg. *, **, <, >) it is considered a "search Sid".
    A Search Sid can resolve to multiple types.
    It is a Typed Sid.

    Notes:
    The Sid's interface is inspired by the pathlib
    https://www.python.org/dev/peps/pep-0428

    #IDEA: implement a class hierarchy
    - BaseSid: any string. By default an empty string.
    - MetaSid: string, may contain meta-characters that can resolve to multiple types
    - TypedSid: has a type and a data dictionary, may contain meta-characters that can resolve to multiple Sids
    - ConcreteSid: describes one single data, that can exist or not
    - DataSid: a sid that may call data sources internally
    - Nice idea >>> Sid('roju', 'a', 'props') -> Sid('roju/a/props')

    #TODO: implement a strict mode that raises Exception if a valid Sid returns a non Sid during an operation like get_with, get_as, /, copy, ...
    """

    def _init(self, string: str = None, type: str = None, data: dict = None):
        # print(f"DataSid._init {string}, {type}, {data}")
        self._string = string or ''
        self._type = type
        self._data = data or dict()

    @property
    def string(self) -> str:
        return self._string

    @property
    def type(self) -> str:
        return self._type

    @property
    def data(self) -> dict:
        return self._data.copy()

    @property
    def full_string(self) -> str:
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').full_string
        "shot__task:roju/s/sq0030/sh0100/animation"

        >>> Sid('blablabla').full_string
        "blablabla"
        """
        return '{}{}'.format(self._type + ':' if self._type else '', self.string)

    @property
    def basetype(self) -> str:
        """
        The basetype is the first part of the type.
        Example:
            for type "shot__file"  -> basetype = "shot"

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').basetype
        "shot"

        :return: string basetype
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
    def keytype(self):
        """
        Returns the last key of the data dictionary.

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
        >>>Sid('roju/a/chars/romeo/modeling').keytype
        "task"

        >>>Sid('roju/s/sq001/sh0010').keytype
        "shot"

        :return: string keytype
        """
        if not self._data:
            warning('[Sid][keytype] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return None
        return list(self._data.keys() or [None])[-1]

    @property
    def parent(self) -> Sid:
        """
        Returns the parent Sid.

        If the
        Returns an empty Sid, if the Sid is not "defined", or self if the Sid is already the root (has no parent).

        Example:
        >>> Sid('roju/s/sq0030/sh0100').parent
        Sid('roju/s/sq0030')
        """
        if not self._data:
            warning('[Sid][parent] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()
        if len(self._data.keys()) == 1:
            return self
        parent_key = list(self._data.keys())[-2]
        return self.get_as(parent_key)

    def __str__(self) -> str:
        return self._string

    def __repr__(self) -> str:
        return 'Sid("{0}")'.format(self.full_string)

    def __hash__(self, *args, **kwargs) -> int:
        return hash(repr(self))

    def __eq__(self, other: Sid | str) -> bool:
        if isinstance(other, Sid):
            return str(other.full_string) == str(self.full_string)
        else:
            return str(other) == str(self)

    def __truediv__(self, other: Sid | str) -> Sid:
        """
        Override the division operator.
        Is this really useful ? Seems nice, but actually dangerous.

        For every Sid:
        >>> sid.parent / sid.get(sid.keytype) == sid
        """
        return Sid(str(self) + conf.sip + str(other))

    def __lt__(self, other: Sid | str) -> bool:
        return str(self) < str(other)

    def __len__(self) -> int:
        return len(self._data)

    def get(self, key: str) -> str | None:
        """
        Returns the value of given key.
        As defined in the internal "data" dictionary.

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').get('shot')
        "sh0100"
        """

        if not self._data:
            warning('[Sid][get] Asked for a Sid operation on an undefined Sid: "{}"'.format(self.string))
            return None

        return self._data.get(key)

    def get_as(self, key: str) -> Sid:
        """
        Returns a new Sid built of the data until (and including) the given key.

        Example:
        >>> Sid('roju/a/chars/romeo/modeling/v001/w/ma').get_as('task')
        Sid('roju/a/chars/romeo/modeling')
        """

        if not self._data:
            warning('[Sid][get_as] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()  # Return type is always Sid.

        data = dict()
        for k, v in self._data.items():
            data[k] = v
            if k == key:
                return Sid(data=data)

        warning(f'[Sid][get_as] Key "{key}" not found in Data "{self._data}"')
        return Sid()

    def get_with(self, uri: str = None, key: str = None, value: str = None, **kwargs) -> Sid:
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
        if not self._data:
            warning(f'[Sid][get_with] Asked for a Sid operation on an undefined Sid "{self.string}"')
            return Sid()  # Return type is always Sid.

        # if we have a uri
        if uri:
            return Sid('{}?{}'.format(self.full_string, uri))

        data_copy = self._data.copy()

        if key:
            kwargs[key] = value
        for key, value in kwargs.copy().items():  # removing a key if the value is None. Use '' for empty values.
            if value is None:
                data_copy.pop(key)
                kwargs.pop(key)

        data_copy.update(kwargs)
        new_sid = Sid(data=data_copy)
        if not new_sid:
            new_sid = Sid('/'.join(list(data_copy.values())))  # FIXME: this is highly guesswork.
        return new_sid

    def as_uri(self) -> str:
        """
        Returns the data as a key value string, as in an URI.


        Example:
        >>>Sid('hamlet/a/char/ophelia/model').as_uri()
        "project=hamlet&type=a&cat=char&name=ophelia&task=model"

        :return: string uri
        """
        return uri_helper.to_string(self._data)

    def copy(self) -> Sid:
        """
        Returns a copy of the current Sid.

        (implementation is experimental, to be improved)
        #TODO: check implementation, to ensure equality.

        >>>Sid('roju/a/chars/romeo/modeling')
        Sid('roju/a/chars/romeo/modeling')

        :return: Sid
        """
        return Sid(self.full_string)  # self.get_with()

    def is_search(self) -> bool:
        """
        Returns True if the current Sid contains search symbols.
        Search symbols are defined in the Sid conf, and are typically: ['*', ',', '>', '<', '**']

        The Sid may not be typed.
        """
        return any(s in str(self) for s in conf.search_symbols)

    def match(self, search_sid: Sid | str) -> bool:  #IDEA: match_as(search_sid, key) for example, do the "seq" of both sids match
        """
        Returns True if a given search_sid matches the current Sid.
        Else False.

        This method is useful to create filters matching groups of Sids, more precise than types.

        Example:
        >>>Sid('roju/a/chars/romeo/modeling').match('roju/a/*/*/modeling')
        True
        >>>Sid('roju/s/sq0030/sh0100/animation').match('roju/s/*/*/*')
        True
        >>>Sid('roju/a/chars/romeo').match('roju/a/props/*')
        False

        :return: bool
        """
        if not self._data:  # Should untyped sids be able to match ? Identical strings could match.
            warning('[Sid][match] Asked for a match check on an undefined Sid: "{}". Returning False.'.format(self.string))
            return False
        from spil import LS
        ls = LS([self.string])
        return ls.get_one(search_sid, as_sid=False) == self.string

    @property
    def path(self) -> os.Pathlike[str]:
        """
        Returns the file path for the current Sid, as a string.
        Returns None if the Sid has no path, or if it cannot be resolved.

        Example:
        >>> Sid('roju/a/chars/romeo/modeling/v001/w/ma').path
        Path("/productions/romeo_juliette/assets/characters/romeo/3d/modeling/works/romeo_v001.ma")

        #TODO: return a Path object? return '' instead of None?
        """
        result = None
        try:
            result = dict_to_path(self._data, self._type)
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result

    def get_last(self, key=None):
        """
        Returns a new Sid object, with the same data as self, and the last existing match for given key.
        If key is not given, the keytype is used.

        Examples:
            >>>Sid('roju/a/chars/romeo/modeling/v001/w/ma').get_last('version')
            Sid('roju/a/chars/romeo/modeling/v008/w/ma')

            >>>Sid('roju/a/chars/romeo/modeling').get_last()
            Sid('roju/a/chars/romeo/shading')

        This method calls Data internally, and is a shortcut to:
            Data().get_one(self.get_with(key=key, value='>'), as_sid=True)

        Note: Sid sorting is currently limited to string values, which usually works with versions.
        A meaningful sorting (eg. "render" after "animation") is planned.

        (implementation is experimental)

        :return: Sid
        """
        if not key:
            key = self.keytype
        from spil import Data as DS  # FIXME: proper delegated sid sorting
        found = DS().get_one(self.get_with(key=key, value='>'), as_sid=True)
        if found.get(key):  # little failsafe. #SMELL
            return found
        else:
            return Sid()

    def get_attr(self, attribute):
        """
        Returns an attribute for the current sid as defined in data_conf.

        Shortcut to data.get(sid, attribute), which is called internally.

        Example:
        >>> Sid('roju/a/chars/romeo/modeling/v001/w/ma').get_attr('comment')
        "first version"
        """
        from spil.data.data import get
        value = get(self, attribute)
        if value:
            return value

    def get_next(self, key):  # FIXME: delegate to Data framework
        """
        This method is experimental. Do not use.

        Returns self with version incremented, or first version if there is no version.
        If version is '*', returns "new" version (next of last)

        If the result is not a valid Sid (not typed, no data), returns an empty Sid.

        :return: Sid
        """
        if key != 'version':
            raise NotImplementedError("get_next() support only 'version' key for the moment.")
        current = self.get('version')
        if current:
            if current in ['*', '>']:  #FIXME: point to "searcher signs" config
                version = (self.get_last('version').get('version') or 'V000').split('V')[-1] or 0
            else:
                version = self.get('version').upper().split('V')[-1]  # temporary workaround for "v001" FIXME
        else:
            version = 0  # allow non existing version #RULE: starts with V001 (#FIXME)
        version = (int(version) + 1)
        version = 'V' + str('%03d' % version)
        result = self.get_with(version=version)
        return result if result else Sid()

    def get_new(self, key):  # FIXME: delegate to Data framework
        """
        This implementation is experimental.

        Returns self with next of last version, or first version if there is no version.

        If the result is not a valid Sid (not typed, no data), returns an empty Sid.

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
        Returns True if the current Sid exists in a datasource.

        Shortcut to Data().exists(sid), which is called internally.

        :return: bool
        """
        from spil import Data as DS
        return DS().exists(self)

    def is_leaf(self):
        """
        Returns True if the current Sid is a leaf node.

        This method is experimental. Implementation and concept to be clarified.

        Note: A leaf should be dependent on the context and type.
        For example, in searching for render files,
        it can be useful to handle the "render pass" as leave,
        to avoid going too deep in the hierarchy.
        This is done in the browser, to browse render files by the pass folder, not individually by default.

        :return: bool
        """
        return bool(self.get('ext'))
        #FIXME: hard coded. Relying on the fact that a leaf has an extention, called "ext".
        # Define "complete". Also in regard to a search Sid. For example Sids containing /** are "complete".
        # or if a Sid has no children, it is leaf.

    def get_uri(self):
        raise DeprecationWarning("get_uri was renamed as_uri")

    # def get_first, get_next, get_previous, get_parent, get_children, project / thing / thing
    # implement URIs: Sid('FTOT').get_with(uri='type=A') <==> FTOT?type=A  ==>  FTOT/A
    # define "complete / incomplete" sid.is_leaf ? (root / anchor / parent / parents /
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent


if __name__ == '__main__':
    from spil_tests import stop
    from pprint import pprint
    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(DEBUG)



