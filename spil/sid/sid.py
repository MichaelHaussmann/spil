# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from collections import OrderedDict

from spil.sid.core import sid_resolver, fs_resolver
from spil.util.log import info, warn, debug

from spil.sid.core.string_resolver import string_to_dict
from spil.sid.core.fs_resolver import dict_to_path
from spil import conf
from spil.util.exception import SpilException

import six
if six.PY3:
    unicode = str
    #import sys  #TODO
    #if sys.version_info[0:2] >= (3, 6):
    #    OrderedDict = dict


class Sid(object):
    """
    A Sid contains 3 values.

    1) A string
    This is the bare minimum for a Sid to exist. By default it is an empty string.

    2) A data dictionary
    If the string matches a defined pattern, the data dictionary is filled.
    It is a Defined Sid / a resolved Sid.

    3) A type
    The matching pattern gives the Sid its type.
    The type is of form basetype__subtype.
    If the Sid contains meta-characters, it is considered a "search Sid".
    A Search Sid can resolve to multiple types.
    It is a Typed Sid.

    """

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Sid("{0}")'.format(str(self))

    def __hash__(self, *args, **kwargs):
        return hash(repr(self))

    def __eq__(self, other):
        return unicode(other) == unicode(self)

    def __len__(self):
        return len(self.data)

    def __define_by_sid(self, sid, do_check=False):

        self.string = str(sid)

        # resolving
        _type, data = sid_resolver.sid_to_dict(self.string)

        if not data:
            info('[Sid] Sid "{}" did not resolve to valid Sid data.'.format(sid))
            return

        if do_check:
            # check if resolves back
            resolved_sid = sid_resolver.dict_to_sid(data, _type)
            if self.string != resolved_sid:
                warn('[Sid] Sid "{}" resolved to valid Sid data, but resolved back to "{}"'.format(sid, resolved_sid))
                return

        self.data = data or OrderedDict()

        if do_check:
            # checking for type uniqueness
            if len(sid_resolver.dict_to_type(self.data, all=True)) > 1:
                warn('[Sid] Sid "{}" matches multiple types. Sid will be untyped.'.format(self.string))
                return

        self.type = _type

    def __define_by_data(self, data, do_check=False):  #TODO: make a fast version when the data comes from an internal trusted and already typed call.

        debug('__define_by_data : {}'.format(data))

        _type = sid_resolver.dict_to_type(data)  # FIXME: terrible code
        if not _type:
            warn('[Sid] Data "{}" did not resolve to valid Sid type.'.format(data))
            return

        # Now getting sid and ordered dict
        self.string = sid_resolver.dict_to_sid(data, _type)
        self.type, data = sid_resolver.sid_to_dict(self.string, _type)

        self.data = data or OrderedDict()

        # TDOD: implement check

    def __define_by_path(self, path, do_check=False):

        # resolving
        _type, data = fs_resolver.path_to_dict(path)

        if not data:
            info('[Sid] Path "{}" did not resolve to valid Sid data.'.format(path))
            return

        # Now getting sid
        resolved_sid = sid_resolver.dict_to_sid(data, _type)
        if not resolved_sid:
            info('[Sid] Path "{}" did resolve to data {}, but not back to Sid'.format(path, data))
            return

        self.string = resolved_sid
        self.data = data or OrderedDict()
        self.type = _type

        # TDOD: implement check

    def __init__(self, sid=None, data=None, path=None, **kwargs):
        """
        Sid Init method.

        In case of multiple arguments, the latter are ignored (if sid s given, data is ignored, if data is given, path is ignored, etc.)
        If no param is given, eg. Sid(), returns an empty Sid().

        :param sid: a Sid object or string
        :param data: a data dictionary
        :param path: a path for a Sid

        TODO: proper kwargs implementation, grabbing custom ad-hoc configs, and also possible sid keys.
        TODO: add type to arguments, to be able to build Sids that keep their type if possible.
        :return:
        """
        self.string = ''
        self.data = OrderedDict()
        self.type = None

        if sid:
            self.__define_by_sid(sid)

        elif data:
            self.__define_by_data(data)

        elif path:
            self.__define_by_path(path)

        elif kwargs:  #FIXME: re-implement kwargs handling and custom string
            key = list(kwargs.keys())[0]
            resolve_conf = conf.string_resolve.get(key)
            # print(key)
            # print(resolve_conf)
            if resolve_conf:
                templates = resolve_conf.get('templates')
                mapping = resolve_conf.get('mapping')
                _type, data = string_to_dict(kwargs.get(key), templates, mapping)
                # print(data)
                self.__define_by_data(data=data)  # FIXME: this is temporary
                # self.__define_by(data=data, _type=_type)

    def get(self, key):

        if not self.data:
            warn('[Sid][get] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
            return None

        return self.data.get(key)

    def get_as(self, key):

        if not self.data:
            warn('[Sid][get_as] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
            return None

        data = OrderedDict()
        for k, v in self.data.items():
            data[k] = v
            if k == key:
                return Sid(data=data)

    def get_with(self, key=None, value=None, **kwargs):
        """
        Returns a Sid with the given key(s) changed.

        Can be called with an key / value pair (if key is set)
        Or via **kwargs to set multiple keys
        Or both.

        :param key: a key name
        :param value: a value for attribute
        :param kwargs: a key/value dictionary
        :return:
        """
        data_copy = self.data.copy()
        if key:
            kwargs[key] = value
        data_copy.update(kwargs)
        return Sid(data=data_copy) or Sid('/'.join(list(data_copy.values())))  # FIXME: test under py27

    @property
    def path(self):
        """
        return the sid as a path
        """
        result = None
        try:
            result = dict_to_path(self.data, self.type)
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result

    @property
    def parent(self):  #YAGNI ?
        """
        Returns the parent Sid, or None if the Sid is not "defined", or an empty Sid if it is already the root. (#TODO: better define the root Sid)
        """
        if not self.data:
            warn('[Sid][parent] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
            return None
        if len(self.data.keys()) == 1:
            return Sid()
        return self.get_as(list(self.data.keys())[-2])

    @property
    def basetype(self):
        """
        return the first part of the type
        """
        result = None
        if not self.type:
            info('This Sid has no type. ({})'.format(self))
            return None
        try:
            result = self.type.split(conf.sidtype_keytype_sep)[0]
        except Exception as e:
            info('[sid][basetype] Unable to get basetype. Sid: {} ("{}")'.format(self, e))
        return result

    @property
    def keytype(self):
        """
        return the last key
        """
        if not self.data:
            warn('[Sid][keytype] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
            return None
        return list(self.data.keys() or [None])[-1]

    """
    def set(self, key=None, value=None, **kwargs):
        if key:
            kwargs[key] = value
        self = self.get_with(**kwargs)
    """

    def copy(self):
        return self.get_with()

    def get_last(self, key):
        from spil import FS  # FIXME: explicit delegation and dynamic import, and proper delegated sid sorting
        return FS().get_one(self.get_with(key=key, value='>'))

    def exists(self):
        from spil import FS  # FIXME: explicit delegation and dynamic import
        return FS().exists(self)

    def match(self, search_sid):
        """
        Returns True if a given search_sid matches the current Sid.
        """
        from spil import LS
        fs = LS([self.string])
        return fs.get_one(search_sid, as_sid=False) == self.string

    def is_leaf(self):
        return bool(self.get('ext'))
        #FIXME: hard coded. Relying on the fact that a leaf has an extention, called "ext".
        # Define "complete". Also in regard to a search Sid. For example Sids containing /** are "complete".

    # def get_first, get_next, get_previous, get_parent, get_children, project / thing / thing
    # define "complete / incomplete" sid.is_leaf ? (root / anchor / parent / parents /
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent


if __name__ == '__main__':

    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(INFO)

    # sid = Sid('raj/s/sq001/sh0020/**/avi')

    sid = 'raj/a/char/juliet/low/design/v002/w/mp4'
    sid = Sid(sid)
    print(sid)
    print(sid.get_last('version'))
    print(sid.parent)
    print(sid.parent.get_last('version'))
    # print(sid.parent.get_last('version').path)
    print()

    sids = ['raj/a/char/juliet/low/design/v002/w/mp4', 'raj/a/char/juliet/low/design/v002']
    match_tests = ['*/*/**/v002/w/movie', '*/*/**/movie', '*/**/movie', 'raj/a,s/*/*/*/*/*']

    for sid in sids:
        for against in match_tests:
            print('{} U {} ? -> {}'.format(sid, against, Sid(sid).match(against)) )
    print()

    print(Sid(sid).match(sid)) # Always True
    print(Sid(against).match(against))  # Should also be always True (#FIXME: SearchSid resolve)

