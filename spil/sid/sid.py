# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from collections import OrderedDict
from functools import total_ordering

from spil.sid.core import sid_resolver, fs_resolver
from spil.sid.core import uri_helper
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


@total_ordering
class Sid(object):
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
    The type is of form basetype__subtype.
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

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Sid("{0}")'.format(self.full_string)

    def __hash__(self, *args, **kwargs):
        return hash(repr(self))

    def __eq__(self, other):
        if isinstance(other, Sid):
            return unicode(other.full_string) == unicode(self.full_string)
        else:
            return unicode(other) == unicode(self)

    if six.PY2:
        #FIXME: handle uri here
        def __div__(self, other):
            return Sid(str(self) + conf.sip + str(other))
    else:
        def __truediv__(self, other):
            """
            Override the division operator.
            Is this really useful ? Seems nice, but actually dangerous.

            For every Sid:
            >>> sid.parent / sid.get(sid.keytype) == sid
            """
            return Sid(str(self) + conf.sip + str(other))

    def __lt__(self, other):
        return unicode(self) < unicode(other)

    def __len__(self):
        return len(self.data)

    @property
    def full_string(self):
        """
        Returns the long string representation of a Sid.
        The form is "type:string" if typed, else just the sid string.

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').full_string
        "shot__task:roju/s/sq0030/sh0100/animation"

        >>> Sid('blablabla').full_string
        "blablabla"
        """
        return '{}{}'.format(self.type + ':' if self.type else '', self.string)

    def __define_by_sid(self, sid, do_check=False):

        # TODO: better handling if Sid is given. Handle as a copy or re-create
        self.string = sid.full_string if isinstance(sid, Sid) else str(sid)

        if self.string.count('?'):  # sid contains URI ending. We put it aside, and later append it back
            string, uri = self.string.split('?', 1)
        else:
            string = self.string
            uri = ''

        # resolving
        if string.count(':'):
            _type, string = string.split(':')
            _type, data = sid_resolver.sid_to_dict(string, _type)
        else:
            _type, data = sid_resolver.sid_to_dict(string)

        if not data:
            info('[Sid] Sid "{}" / {} / {} did not resolve to valid Sid data.'.format(sid, self.string, string))
            return

        if do_check:
            # check if resolves back
            resolved_sid = sid_resolver.dict_to_sid(data, _type)
            if string != resolved_sid:
                warn('[Sid] Sid "{}" resolved to valid Sid data, but resolved back to "{}"'.format(sid, resolved_sid))
                return

        self.data = data or OrderedDict()

        if do_check:
            # checking for type uniqueness
            if len(sid_resolver.dict_to_type(self.data, all=True)) > 1:
                warn('[Sid] Sid "{}" matches multiple types. Sid will be untyped.'.format(self.string))
                return

        self.type = _type

        # integrating the uri, and updating the type
        if not uri:
            self.string = string  # string without type, without uri
        else:
            """
            uri integration algorithm:
            - the URI key/values are applied to the existing data dict --> uri_helper.update
            - the data dictionary is submitted to type resolve --> sid_resolver.dict_to_type(data, all=True)
            - if a single type is resolved, it is now used, integration done.
            - else if no type is resolved, the URI is not applied (kept in the string, the data and type are unchanged)
            - else if multiple types are resolved, the URI is not applied (kept in the string, the previous data and type are unchanged)
            
            This is a problem in case of a search Sid, which could be poly-typed.
            """
            data = uri_helper.update(self.data, uri)
            _type = sid_resolver.dict_to_type(data, all=True)
            if not _type:
                warn('[Sid] After URI apply, Sid "{}" has no type. URI will not be applied.'.format(self.string))
                self.string = '{}?{}'.format(string, uri)
                return
            if len(_type) > 1:
                if self.type not in _type:
                    if any(s in '{}?{}'.format(string, uri) for s in conf.search_symbols):
                        debug(
                            '[Sid] After URI apply, Sid "{}" matches different types: {}. But it is a Search, so URI will be applied.'.format(
                                self.string, _type))
                    else:
                        warn('[Sid] After URI apply, Sid "{}" matches different types: {}. URI will not be applied.'.format(self.string, _type))
                        self.string = '{}?{}'.format(string, uri)
                        return
                else:  # URI apply still matches previously given type
                    _type = [self.type]
            # updated data is OK
            string = sid_resolver.dict_to_sid(data, _type[0])
            if string:
                self.data = data
                self.type = _type[0]
                self.string = string

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

        #TODO:
        - create a factory method to simplify Sid constructor
          (allowing simplifications like new_sid.get_with(**to_dict(uri)))
        - streamline URI and type implementation (type and uri arguments, enable "sid = Sid(sid)"
        - proper kwargs implementation for "string_resolve", grabbing custom ad-hoc configs, and also possible sid keys.
        - add getters that traverse formatting mappings, eg get('project', 'longname') / get('project', 'foldername')

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
        """
        Returns the value of given key.
        As defined in the internal "data" dictionary.

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').get('shot')
        "sh0100"
        """

        if not self.data:
            warn('[Sid][get] Asked for a Sid operation on an undefined Sid: "{}"'.format(self.string))
            return None

        return self.data.get(key)

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

    def get_as(self, key):
        """
        Returns a new Sid built of the data until (and including) the given key.

        Example:
        >>> Sid('roju/a/chars/romeo/modeling/v001/w/ma').get_as('task')
        Sid('roju/a/chars/romeo/modeling')
        """

        if not self.data:
            warn('[Sid][get_as] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()  # Return type is always Sid.

        data = OrderedDict()
        for k, v in self.data.items():
            data[k] = v
            if k == key:
                return Sid(data=data)

        warn('[Sid][get_as] Key "{}" not found in Data "{}"'.format(key, self.data))
        return Sid()

    def get_with(self, key=None, value=None, **kwargs):
        """
        Returns a new Sid with the given key(s) changed.
        A key set to None will be removed - thus potentially changing the type.
        To empty a keys value, set it to an empty string "".

        Can be called with an key / value pair (if key is set)
        Or via **kwargs to set multiple keys
        Or both.

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').get_with(task='rendering')
        Sid('roju/s/sq0030/sh0100/rendering')

        :param key: a key name
        :param value: a value for attribute
        :param kwargs: a key/value dictionary
        :return:
        """
        if not self.data:
            warn('[Sid][get_with] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()  # Return type is always Sid.

        data_copy = self.data.copy()

        # if we have a single param, we treat is as a URI
        if key and not any([value, kwargs]):
            return Sid('{}?{}'.format(self.full_string, key))

        if key:
            kwargs[key] = value
        for key, value in six.iteritems(kwargs.copy()):  # removing a key if the value is None. Use '' for empty values.
            if value is None:
                data_copy.pop(key)
                kwargs.pop(key)
        data_copy.update(kwargs)
        return Sid(data=data_copy) or Sid('/'.join(list(data_copy.values())))  # FIXME: test under py27

    @property
    def path(self):
        """
        Returns the file path for the current Sid, as a string.
        Returns None if the Sid has no path, or if it cannot be resolved.

        Example:
        >>> Sid('roju/a/chars/romeo/modeling/v001/w/ma').path
        "/productions/romeo_juliette/assets/characters/romeo/3d/modeling/works/romeo_v001.ma"

        #TODO: return a Path object? return '' instead of None?
        """
        result = None
        try:
            result = dict_to_path(self.data, self.type)
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result

    @property
    def parent(self):
        """
        Returns the parent Sid.
        Returns an empty Sid, if the Sid is not "defined", or self if the Sid is already the root (has no parent).

        Example:
        >>> Sid('roju/s/sq0030/sh0100').parent
        Sid('roju/s/sq0030')
        """
        if not self.data:
            warn('[Sid][parent] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return Sid()
        if len(self.data.keys()) == 1:
            return self
        return self.get_as(list(self.data.keys())[-2])

    @property
    def basetype(self):
        """
        The basetype is the first part of the type.
        Example:
            for type "shot__file"  -> basetype = "shot"

        Example:
        >>> Sid('roju/s/sq0030/sh0100/animation').basetype
        "shot"

        :return: string basetype
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
        Returns the last key of the data dictionary.

        Examples:
        >>>Sid('roju/a/chars/romeo/modeling').keytype
        "task"

        >>>Sid('roju/s/sq001/sh0010').keytype
        "shot"

        :return: string keytype
        """
        if not self.data:
            warn('[Sid][keytype] Asked for a Sid operation on an undefined Sid "{}"'.format(self.string))
            return None
        return list(self.data.keys() or [None])[-1]

    def copy(self):
        """
        Returns a copy of the current Sid.

        (implementation is experimental, to be improved)
        #TODO: check implementation, to ensure equality.

        >>>Sid('roju/a/chars/romeo/modeling')
        Sid('roju/a/chars/romeo/modeling')

        :return: Sid
        """
        return Sid(self.full_string)  # self.get_with()

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

    def get_uri(self):  # TODO: unify string, data, uri, fullstring accesses. sid.get_uri returns the uri part, not the sid as_uri
        """
        Returns the data as a key value string, as in an URI.

        The name of this method will likely change!

        Usage still experimental.
        #TODO: (method name to be improved)

        Example:
        >>>Sid('roju/a/chars/romeo/modeling').get_uri()
        "project=roju&type=a&cat=chars&name=romeo&task=modeling"

        :return: string uri
        """
        return uri_helper.to_string(self.data)

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

    def exists(self):
        """
        Returns True if the current Sid exists in a datasource.

        Shortcut to Data().exists(sid), which is called internally.

        :return: bool
        """
        from spil import Data as DS
        return DS().exists(self)

    def match(self, search_sid):  #IDEA: match_as(search_sid, key) for example, do the "seq" of both sids match
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
        if not self.data:  # Should untyped sids be able to match ?
            warn('[Sid][match] Asked for a match check on an undefined Sid: "{}". Returning False.'.format(self.string))
            return False
        from spil import LS
        ls = LS([self.string])
        return ls.get_one(search_sid, as_sid=False) == self.string

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

    def is_search(self):
        """
        Returns True if the current Sid contains search symbols.
        Search symbols are defined in the Sid conf, and are typically: ['*', ',', '>', '<', '**']

        The Sid may not be typed.
        """
        return any(s in str(self) for s in conf.search_symbols)

    # def get_first, get_next, get_previous, get_parent, get_children, project / thing / thing
    # implement URIs: Sid('FTOT').get_with(uri='type=A') <==> FTOT?type=A  ==>  FTOT/A
    # define "complete / incomplete" sid.is_leaf ? (root / anchor / parent / parents /
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent


if __name__ == '__main__':

    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(INFO)

    # Test get_new('version')
    sid = 'FFM/S/SQ0001/SH0040/HFXout-MOCCO'
    sid = Sid(sid)
    new_scene = sid.get_with(version='*', state='WIP', ext='ma')
    print(new_scene.type)
    # print(new_scene.get_new('version'))


    sid = 'FTOT?type=A'
    sid = 'FTOT?project=FTOT&type=A'
    sid = Sid('FTOT?project=FTOT&type=A')
    assert sid == Sid(sid.get('project') + '?' + sid.get_uri())

    # sid = Sid('raj/s/sq001/sh0020/**/avi')

    sid = 'raj/a/char/juliet/low/design/v002/w/mp4'
    sid = Sid(sid)
    print(sid)
    print(sid.get_last('version'))
    # print(sid.get_next('version'))
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

