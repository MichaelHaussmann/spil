# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

# TODO : refacto into class
# TODO : use explicit project in resolve process, so we can have one configuration per project.
from collections import OrderedDict

import six

if six.PY3:
    import spil.vendor  # SMELL
import lucidity
from lucidity import Template

from spil.util.log import debug
from spil.conf import sidtype_keytype_sep, key_types  # TODO: default confs to avoid editor errors

# would it be nice to retrieve a sid in the native format also (mapping back + format, like to FT) ?
# that's not how we create the data inside the target system .... unless we do ?

"""
String resolver

Is the low level under the Sid object.

Transforms a given string into a valid sid dict

"""


def string_to_dict(string, string_templates, mapping={}):

    # instantiating lucidity Templates
    templates = []
    for name, pattern in six.iteritems(string_templates):
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        # template.template_resolver = resolvers
        templates.append(template)

    # try template parse
    try:
        data, template = lucidity.parse(str(string), templates)
        # print('found {} {}'.format(data, template))
    except lucidity.ParseError as e:
        debug(e)
        return None, None

    if not data:
        return None, None

    # value mapping
    for key, value in six.iteritems(data):
        if mapping.get(key):
            value = mapping.get(key).get(value, value)
            data[key] = value

    # Sorting the result data into an OrderedDict()
    _type = template.name.split(sidtype_keytype_sep)[0]
    keys = key_types.get(_type)  # using template to get sorted keys
    keys = filter(lambda x: x in template.keys(), keys)  # template.keys() is a set

    data = data.copy()
    ordered = OrderedDict()
    for key in keys:
        ordered[key] = data.get(key)

    return template.name, ordered


if __name__ == '__main__':

    """
    This is currently not used. 
    A specific mapping needs to be configured for this to work.

    """

    tests = ['FTRACK_TEST_PROJECT/02_shots/sq0001/sq0001_sh0010/layout/V001/w',
            'FTRACK_TEST_PROJECT/02_shots/sq0001/sq0001_sh0010/layout/V003/w',
            'FTRACK_TEST_PROJECT/01_assets/01_char/romeo/mdl/v001/w',
            'FTRACK_TEST_PROJECT/02_shots/sq0001/sq0001_sh0020/layout/V001/w',
            'FTRACK_TEST_PROJECT/02_shots/sq0001/sq0001_sh0020/layout/V008/w']

    from spil.util.log import setLevel, INFO, info
    from spil.conf import ft_templates, ft_mapping

    info('Tests start')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    for test in tests:

        info('*' * 15)
        info('Testing : {}'.format(test))

        _type, _dict = string_to_dict(test, ft_templates, ft_mapping)
        info('sid {} ---> \n{}'.format(test, _dict))


        info('*'*15)
        print('  ')

    info('*' * 30)
    info('*' * 30)
