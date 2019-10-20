# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


Sid resolver

Is the low level under the Sid object.

Transforms the sid string into a valid sid dict, and reverse.

"""

# TODO : refacto into class
# TODO : use explicit project in resolve process, so we can have one configuration per project.

import six

if six.PY3:
    import spil.vendor
import lucidity

from spil.libs.util.log import debug, warn
from spil.libs.util.exception import SpilException

# sid conf
from spil.conf.sid_conf import sip
from spil.conf.sid_conf import sid_templates, sid_filters, get_sidtype, meta_items


def parse_sid(sid, pattern, name='template'):

    template = lucidity.Template(name, pattern,
                                 default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                                 anchor=lucidity.Template.ANCHOR_BOTH)

    diff = template.pattern.count(sip) - sid.count(sip)  # allowing sids to be open at the end
    if diff > 0:
        sid = sid + sip * diff

    try:
        data = template.parse(sid)
        debug('{} matched template "{}"'.format(sid, name))
        return data

    except Exception as e:
        debug('{} did not match template "{}" (error:{})'.format(sid, name, e))

        return None


def validate_sid(data, filters):
    """
    Validates the data via filters.
    meta_items are not filtered.

    :param data:
    :param filters:
    :return:
    """
    if not filters:
        debug('No filter was given, data auto validated : {}'.format(data))
        return True

    if not data:
        return False

    if not data.keys():
        return False

    data = data.copy()

    for key, value in six.iteritems(data.copy()):
        if value in meta_items:
            continue
        if value and filters.get(key):
            if not filters.get(key)(value):
                return False
        if not value:
            data.pop(key)

    return True


def sid_to_dict(sid):

    sid = str(sid)

    debug('[sid_to_dict] : {}'.format(sid))

    # checking asset : resolving by template, then validating
    asset_data = parse_sid(sid, sid_templates.get('asset'), name='asset')
    if not asset_data:
        debug('sid "{}" not matching an asset template'.format(sid))
    asset_valid = validate_sid(asset_data, sid_filters.get('asset'))
    if not asset_valid:
        debug('sid "{}" not validated using asset filters'.format(sid))

    # checking shots : resolving by template, then validating
    shot_data = parse_sid(sid, sid_templates.get('shot'), name='shot')
    if not shot_data:
        debug('sid "{}" not matching a shot template'.format(sid))
    shot_valid = validate_sid(shot_data, sid_filters.get('shot'))
    if not shot_valid:
        debug('sid "{}" not validated using shot filters'.format(sid))

    # checking project : resolving by template, then validating
    project_data = parse_sid(sid, sid_templates.get('project'), name='project')
    if not project_data:
        debug('sid "{}" not matching a project template'.format(sid))
    project_valid = validate_sid(project_data, sid_filters.get('project'))
    if not project_valid:
        debug('sid "{}" not validated using project filters'.format(sid))

    result = [asset_valid, shot_valid, project_valid]

    if not any(result):
        debug('sid "{}" was not resolved'.format(sid))
        return {}

    if all(result):
        warn('Unable to define basetype for sid "{}"'.format(sid))

    # default resolving to asset first
    if asset_valid:
        debug('sid "{}" was resolved as asset. Result'.format(sid))
        return asset_data

    if shot_valid:
        return shot_data

    if project_valid:
        return project_data


def dict_to_sid(data):

    data = data.copy()

    if not data:
        raise SpilException('[dict_to_sid] Data is empty')

    subtype = get_sidtype(data).split('_')[0]
    pattern = sid_templates.get(subtype)

    if not pattern:
        raise SpilException(
            '[dict_to_sid] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(subtype, data))

    template = lucidity.Template(subtype, pattern)

    if not template:
        raise SpilException('toe')

    sid = template.format(data).rstrip(sip)

    return sid


if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('Tests start')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.sid_conf import test_sids as tests

    for test in tests:

        info('Testing : {}'.format(test))

        _dict = sid_to_dict(test)
        info('sid {} ---> {}'.format(test, _dict))
        _type = get_sidtype(_dict)
        info('type : ' + _type)

        retour = dict_to_sid(_dict)
        info('retour: ' + retour)

        assert(test == retour)

        info('*'*15)

    info('*' * 30)
    info('*' * 30)
