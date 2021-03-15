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
from spil.util.log import info, warn

from spil.sid.core.string_resolver import string_to_dict
from spil.sid.core.fs_resolver import dict_to_path
from spil import conf
from spil.util.exception import SpilException

import six
if six.PY3:
    unicode = str


class Sid(object):

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Sid("{0}")'.format(str(self))

    def __hash__(self, *args, **kwargs):
        return hash(repr(self))

    def __eq__(self, other):
        return unicode(other) == unicode(self)

    def __init__(self, sid=None, data=None, path=None, **kwargs):
        """
        Sid Init method.

        If sid is given, data is ignored.
        If no param is given, eg. Sid(), returns an empty Sid().

        :param sid: a Sid object or string
        :param data: a data dictionary
        :return:
        """

        self.string = ''  # sid string form, also "path". IDEA: implement as a Path() ? Inherit from pathlib ?
        self.data = OrderedDict()
        self.keytype = None

        if sid:
            self.string = str(sid)
            _keytype, data = sid_resolver.sid_to_dict(self.string)
            # info(_keytype)
            # info(data)
            if data:
                check = sid_resolver.dict_to_sid(data, _keytype)
                if check == self.string:
                    self.data = data
                    self.keytype = _keytype
                else:
                    warn('[Sid] Sid "{}" resolved to valid Sid data of type "{}", but resolved back to "{}"'.format(sid, _keytype, check))
            else:
                warn('[Sid] Sid "{}" did not resolve to valid Sid data.'.format(sid))

        elif data:

            sid = sid_resolver.dict_to_sid(data)
            if sid:
                _keytype, ordered = sid_resolver.sid_to_dict(sid)
                if ordered and set(data.keys()) == set(ordered.keys()):
                    self.string = sid
                    self.data = ordered
                    self.keytype = _keytype
                else:
                    warn('[Sid] Data "{}" resolved to valid Sid "{}", could not properly resolve back to data.'.format(data, sid))
            else:
                warn('[Sid] Data "{}" did not resolve to valid Sid.'.format(data))

        elif path:
            # self.type, self.data = path_to_dict(path)
            __, data = fs_resolver.path_to_dict(path)

            if data:  # FIXME: refacto
                sid = sid_resolver.dict_to_sid(data)
                if sid:
                    _keytype, ordered = sid_resolver.sid_to_dict(sid)  # resolve back - is this really necessary ?
                    if ordered and set(data.keys()) == set(ordered.keys()):
                        self.string = sid
                        self.data = ordered
                        self.keytype = _keytype
                    else:
                        warn(
                            '[Sid] Data "{}" resolved to valid Sid "{}", could not properly resolve back to data.'.format(
                                data, sid))
                else:
                    warn('[Sid] Data "{}" did not resolve to valid Sid.'.format(data))

        elif kwargs:
            key = list(kwargs.keys())[0]
            resolve_conf = conf.string_resolve.get(key)
            # print(key)
            # print(resolve_conf)
            if resolve_conf:
                templates = resolve_conf.get('templates')
                mapping = resolve_conf.get('mapping')
                __, data = string_to_dict(kwargs.get(key), templates, mapping)
                # print(data)

            if data:
                sid = sid_resolver.dict_to_sid(data)
                if sid:
                    _keytype, ordered = sid_resolver.sid_to_dict(sid)  # resolve back - is this really necessary ?
                    if ordered and set(data.keys()) == set(ordered.keys()):
                        self.string = sid
                        self.data = ordered
                        self.keytype = _keytype
                    else:
                        warn(
                            '[Sid] Data "{}" resolved to valid Sid "{}", could not properly resolve back to data.'.format(
                                data, sid))
                else:
                    warn('[Sid] Data "{}" did not resolve to valid Sid.'.format(data))

    def get(self, key):

        if not self.data:
            warn('[Sid] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
            return None

        return self.data.get(key)

    def get_as(self, key):

        if not self.data:
            warn('[Sid] Asked for a Sid operation on an undefined Sid ({})'.format(self.string))
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
        return Sid(data=data_copy)

    @property
    def path(self):
        """
        return the sid as a path
        """
        result = None
        try:
            result = dict_to_path(self.data, self.keytype)
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result


if __name__ == '__main__':

    pass
