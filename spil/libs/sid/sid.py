# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import functools

import six
import attr

# from spil libs
from spil.libs.util.log import debug, info, warn
from spil.libs.util.exception import SpilException

# from fs
from spil.libs.fs.core.fs_resolver import path_to_dict, dict_to_path

# from sid
from spil.libs.sid.core import sid_resolver
from spil.libs.sid.core.sid_helper import compare_by_template

# Sid config
from spil.conf.project_conf import projects, project_order
from spil.conf.sid_conf import values_sorted, basetype_order
from spil.conf.sid_conf import values_defaults, optional_keys
from spil.conf.sid_conf import project_config, asset_config, shot_config, get_sidtype
from spil.conf.sid_conf import sip


@functools.total_ordering
class BaseSid(object):
    """
    Base class for the Sid classes.
    Contains the functions.

    TODO : getters / setters on make_class Classes.
    """

    # Utilities

    def is_shot(self):
        return self.basetype() == 'shot'

    def is_asset(self):
        return self.basetype() == 'asset'

    @property
    def project_long(self):
        try:
            return projects[self.project].get('long_name')
        except KeyError:
            raise SpilException('Sid malformed, project "{0}" unknown'.format(self.project))

    @property
    def keys(self):
        return self._keys

    @property
    def path(self):
        result = None
        try:
            result = dict_to_path(self.asdict())
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result

    # Returns useful string representations

    def nice(self, sep='/'):
        return str(self).replace(sip, sep)

    def flat(self):  # Keeps only values that are set
        sid = filter(None, [getattr(self, p) for p in self._keys])
        return '_'.join([str(x) for x in sid])

    def get(self, attribute):
        if str(attribute) not in self._keys:
            warn('Attribute... "{}" not in Sid definition of {}. Return None'.format(attribute, self))
            return None
        return getattr(self, attribute)

    def set(self, attribute, value):
        if str(attribute) in self._keys:
            setattr(self, attribute, value)
        else:
            warn('Attribute... "{}" not in Sid definition of {}. Skipped'.format(attribute, self))

    def set_defaults(self, attribute=None, force=None):
        """
        Sets the default values on empty fields, for this sid, as configured.

        If attributes is given, only the given attributes default are set.
        Else, all are set.

        If force is True, already set attributes are overriden with their defaults.
        Else, no attribute is overriden if exists.
        Defaults to False.

        :param attributes: a list or a single attribute to set to default value
        :param force: if attributes with values should be overriden to defaults
        :return:
        """
        #if attributes and not is_sequence(attributes): attributes = [attributes]

        attributes = [attribute] if attribute else list(values_defaults.get(self.basetype(), {}))
        for attribute in attributes:
            if force or not self.get(attribute):
                value = values_defaults.get(self.basetype()).get(attribute)
                self.set(attribute, value)
                debug('Set {} to default value {}'.format(attribute, value))

    def get_as(self, attribute):
        """
        Returns a copy of the Sid as the given attribute.
        Calls copy(until=attribute).

        Example:
        sid.get_as('task')  # Returns a Sid of type task.

        :param attribute:
        :return:
        """
        if not self.has_a(attribute):
            warn('Asked for a "{}" sid, but sid is incomplete. Returning None'.format(attribute))
            return None
        return self.copy(until=attribute)

    def get_with(self, attribute=None, value=None, **kwargs):
        """
        Returns a Sid with the given attribute(s) changed.

        Can be called with an attribute / value pair (if attribute is set)
        Or via **kwargs to set multiple attributes
        Or both.

        :param attribute: an attribute name
        :param value: a value for attribute
        :param kwargs: a attribute/value dictionary
        :return:
        """
        sid_copy = self.copy()
        if attribute:
            kwargs[attribute] = value
        for attribute, value in six.iteritems(kwargs):
            if attribute not in self._keys:
                warn('Attribute "{}" not in Sid definition. Skipped'.format(attribute))
                continue
            setattr(sid_copy, attribute, value)
        return sid_copy

    def has_a(self, attribute):
        """
        Checks whether the Sid contains a complete Sid of given attribute.
        Calls is_complete(until=attribute)

        Example:
        sid.has_a('task')  # Returns True if all is set until task.

        :param attribute:
        :return:
        """
        return self.is_complete(until=attribute)

    def values(self):
        """
        Returns a list of all values.
        Empty values may be included.

        :return:
        """
        return [getattr(self, p) for p in self._keys]

    def parent(self, set_default=False):
        """
        Returns the parent sid.
        Does not return the parent value, but the full parent Sid.

        Sets defaults if set_default is True.
        Useful because the parent may have its last key empty, which might be unexpected.

        Example:
        Sid('demo|s|010|120|animation').parent()  # Will return the Shot Sid 'demo|s|010|120'
        sid.parent()

        Uses get_as().

        :param set_default:
        :return:
        """
        if len(self) <= 1:
            info('Sid {} has no parent. Copy is returned.'.format(self))
            return self.copy()
        parent_key = self._keys[len(self) - 2]
        if set_default:
            self.set_defaults(parent_key)
        return self.get_as(parent_key)

    def copy(self, until=None):
        """
        Returns a copy of the current Sid.
        The copy is always of the same class as the copied.

        If until is given, parameters after until are nulled.

        :param until:
        :return:
        """

        # Full copy
        if not until:
            return self.__class__(**self.asdict())

        # Copy not possible, wrong until
        elif until not in self._keys:
            msg = '[Sid.copy] Given "until" "{0}" is not a key of this sid "{1}".'.format(until, self)
            raise SpilException(msg)

        # we make a full copy, and empty the attributes after "until"
        result = self.__class__(**self.asdict())

        index = self._keys.index(until) + 1
        for attribute in self._keys[index:]:
            setattr(result, attribute, None)

        return result

    def is_complete(self, until='project'):
        """
        Checks if a Sid is complete - all keys have values (all attributes return True) - until a given attribute.

        Intermediate optional keys are ignored.

        @param until: the last attribute that is checked
        """
        for key in self._keys:
            if not getattr(self, key):
                if key not in optional_keys:
                    return False
            if key == until:
                return bool(getattr(self, key))
        warn('[Sid] could not verify completeness of self "{0}" until "{1}"'.format(self, until))
        return False  # malformed or until malformed?

    def last_key(self):
        return self._keys[len(self) - 1]

    # overrides

    def __len__(self):
        """
        Returns the length of the sid, relying on is_complete.
        """
        index = len(self._keys)
        for p in reversed(self._keys):
            if self.is_complete(until=p):
                return index
            else:
                index = index-1
        return 0

    def __str__(self):
        return sid_resolver.dict_to_sid(self.asdict())

    def __repr__(self):
        return 'Sid("{0}")'.format(str(self))  # FIXME: possible class switching

    def __hash__(self, *args, **kwargs):
        return hash(repr(self))

    def __eq__(self, other):
        return self._compare(other) == 0

    def __lt__(self, other):
        return self._compare(other) < 0

    def __iter__(self):
        """
        Iterates over the Sids values.
        Stops at the first mandatory empty value.

        :return: Iterator
        """
        for x in [getattr(self, p) for p in self._keys]:
            if x or x in optional_keys:
                yield x

    def __nonzero__(self):
        """
        Conversion to bool.
        At least the project needs to be defined for the sid to be "True"
        """
        return all([self.project])

    def __add__(self, other):
        """
        Adds a value at the end of the Sid and returns the result.

        If the Sid is complete, a copy is returned without anything added.

        :param other:
        :return:
        """
        if len(self) == len(self._keys):
            warn('Sid {} is already complete. Concatenation impossible.'.format(self))
            return self.copy()
        other = str(other)
        if not other.startswith(sip):
            other = sip + other
        result = str(self) + other
        return Sid(result)

    def _compare(self, other):
        """
        Compares 2 sids hierarchically.

        First compares the projects, than the types.
        If they are not equal, as per configuration, the result is returned.

        If project and types are equal, each sid key is evaluated against the counterpart in the other sid.
        In case of equality, the next key is evaluated, until a greater value is found, and the result is returned.

        For each key, the comparison uses the configuration, or string comparison.

        Uses compare_by_template, where the template comes from the config.

        #IDEA : delegate this to an external comparing function, for example the FileSystem (by dates), or a database.
        In this case, the delegate must only be imported on-demand, since it would be slower than string comparisons.

        :param other: another Sid or Sid string
        :return:
        """
        if str(other) == str(self):
            return 0

        a = self

        # if b is a string, transform to Sid first.
        if isinstance(other, BaseSid):
            b = other
        else:
            b = Sid(other)

        # first compare projects
        compared = compare_by_template(a.project, b.project, project_order)
        if compared != 0:
            return compared

        # then compare the sid types
        compared = compare_by_template(a.basetype(), b.basetype(), basetype_order)
        if compared != 0:
            return compared

        # now looping of the sid keys, until discrimination
        sorted_values = values_sorted.get(a.basetype(), {})  # TODO: bad conf error handling (not just default to {})
        for i, (ia, ib) in enumerate(zip(a, b)):
            if not ia and ib:
                continue
            template = sorted_values.get(a._keys[i])
            compared = compare_by_template(ia, ib, template)
            if compared != 0:
                return compared
        return -1

    def asdict(self):
        """
        A dictionary representation of the current Sid.

        (Generated by attr)

        :return:
        """
        return attr.asdict(self, filter=lambda attr, value: attr.name != '_keys')

    def sidtype(self):
        """
        Complete sid type as defined in sid_conf.get_sidtype()

        Example:
        "asset_task"  # is the type of a Sid that is complete until "task"

        :return: String sid type
        """
        return get_sidtype(self.asdict())

    def basetype(self):
        """
        Returns the first element of the Sid type

        Example:
        "asset" is the first element of "asset_task"

        :return:
        """
        return self.sidtype().split('_')[0]

    def endtype(self):
        """
        Returns the last element of the Sid type

        Example:
        "task" is the last element of "asset_task"

        :return:
        """
        return self.sidtype().split('_')[-1]


ProjectSid = attr.make_class("ProjectSid", project_config, bases=(BaseSid,), cmp=False)
AssetSid = attr.make_class("AssetSid", asset_config, bases=(ProjectSid,), cmp=False)
ShotSid = attr.make_class("ShotSid", shot_config, bases=(ProjectSid,), cmp=False)


def Sid(sid=None, data=None, path=None):
    """
    Sid Factory method :
    Returns a ProjectSid, AssetSid or ShotSid.

    If multiple parameters are given, data is overriden by path, which is overriden by sid.
    If no param is given, eg. Sid(), returns an empty ProjectSid().


    This Sid() factory is not mandatory.
    It is possible to instanciate a Sid directly, eg :
    ShotSid(project='demo', seq='s010', shot='p010', task='04_fx', version='v001', state='w', ext='hip')
    ShotSid(project='demo', seq='s010', shot='p010')

    :param sid: a Sid object or string
    :param data: a data dictionary
    :param path: a valid path
    :return:
    """
    if path:
        _type, data = path_to_dict(path)

    if sid:
        if isinstance(sid, ProjectSid):
            return sid.copy()
        else:
            data = sid_resolver.sid_to_dict(sid)
            # print 'resolved ', sid, data

    if data:
        _type = get_sidtype(data)

        if _type.startswith('asset'):
            return AssetSid(**data)

        elif _type.startswith('shot'):
            return ShotSid(**data)

        else:
            data = {'project': data.get('project')}
            return ProjectSid(**data)

    return ProjectSid()


if __name__ == '__main__':

    info('tests are in the spil.tests package')

    toto = Sid(path= '/home/mh/spil/projects/demo/work/01_assets/characters/dragon')
    toto.project = 'demo'
    info(toto.project_long)
    info(toto.basetype())
    info(toto.path)
    info(repr(toto))
    info(type(Sid()))
    info(Sid())
