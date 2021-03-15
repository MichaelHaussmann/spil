# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import six

from tests import test_00_init
print(test_00_init)

from spil.conf import sid_templates, path_templates
from spil.util.log import info
from warnings import warn


def test_sid_duplicates():

    info('Testing duplicates in sid_templates (sid_conf)')

    sid_keys = set(sid_templates.keys())

    if len(sid_keys) != len(sid_templates.keys()):
        warn('Duplicate keys in sid_templates (sid_conf)')
    else:
        info('Keys OK in sid_templates (sid_conf)')

    if len(set(sid_templates.values())) != len(sid_templates.values()):
        warn('Duplicate values in sid_templates (sid_conf)')
    else:
        info('Values OK in sid_templates (sid_conf)')


def test_fs_duplicates():

    info('Testing duplicates in path_templates (fs_conf)')

    fs_keys = set(path_templates.keys())

    if len(fs_keys) != len(path_templates.keys()):
        warn('Duplicate keys in path_templates (fs_conf)')
    else:
        info('Keys OK in path_templates (fs_conf)')

    if len(set(path_templates.values())) != len(path_templates.values()):
        warn('Duplicate values in path_templates (fs_conf)')
        for val in sorted(path_templates.values()):
            print(val)
    else:
        info('Values OK in path_templates (fs_conf)')


def test_missings():

    info('Testing missings in sid_conf vs fs_conf')

    sid_keys = set(sid_templates.keys())
    fs_keys = set(path_templates.keys())

    to_ignore = {'project_root'}

    missing_in_fs_conf = sid_keys - fs_keys - to_ignore
    if missing_in_fs_conf:
        warn('Missing in fs_conf (path_templates) : {}'.format(missing_in_fs_conf))

    missing_in_sid_conf = fs_keys - sid_keys - to_ignore
    if missing_in_sid_conf:
        warn('Undefined in sid_conf (sid_templates) : {}'.format(missing_in_sid_conf))
    else:
        info('')


if __name__ == '__main__':

    print()
    print('Sid Templates: ')
    for k, v in six.iteritems(sid_templates):
        print('{} -> {}'.format(k, v))

    print()
    print('Path Templates: ')
    for k, v in six.iteritems(path_templates):
        print('{} -> {}'.format(k, v))

    print()
    print('Tests: ')
    test_sid_duplicates()
    test_fs_duplicates()
    test_missings()

    print('Done')



