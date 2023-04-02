# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
Global configuration test.

Shows what may be duplicate, and what is missing from either config_name (sid, fs)

"""
import spil  # default config bootstrap

from spil.conf import sid_templates  # type: ignore
from spil.sid.pathops.pathconfig import get_path_config
path_config = get_path_config()
path_templates = path_config.path_templates

from spil.util.log import DEBUG, ERROR, get_logger
log = get_logger('tests')
log.setLevel(DEBUG)


def test_show_config():

    log.debug('Starting')
    log.debug('Path Templates: ')
    for k, v in path_templates.items():
        log.info('{} -> {}'.format(k, v))


def get_duplicates(items):
    unique = set()
    duplicate = set()
    for item in items:
        if item not in duplicate:
            unique.add(item)
        else:
            duplicate.add(item)
    return duplicate


def test_fs_duplicates():

    log.debug('- Testing duplicates in path_templates (fs_conf)...')

    duplicate_keys = get_duplicates(path_templates.keys())
    if duplicate_keys:
        log.warning('\tFAILED: Duplicate keys in path_templates (fs_conf): {}'.format(duplicate_keys))
    else:
        log.info('\tOK: No duplicate in path_templates keys (fs_conf).')

    duplicate_values = get_duplicates(path_templates.values())
    if duplicate_values:
        log.warning('\tFAILED: Duplicate values in path_templates (fs_conf): {}'.format(duplicate_values))
    else:
        log.info('\tOK: No duplicate in path_templates values (fs_conf).')

    log.debug('done')


def test_missing():

    log.debug('- Testing missing in sid_conf vs fs_conf...')

    sid_keys = set(sid_templates.keys())
    fs_keys = set(path_templates.keys())

    to_ignore = {'project_root'}

    missing_in_fs_conf = sid_keys - fs_keys - to_ignore
    if missing_in_fs_conf:
        log.warning('\tFAILED: Missing sid_conf keys in FS keys: {}'.format(missing_in_fs_conf))
    else:
        log.info('\tOK: all sid_conf keys are in FS keys.')

    missing_in_sid_conf = fs_keys - sid_keys - to_ignore
    if missing_in_sid_conf:
        log.warning('\tFAILED: Missing FS keys in sid_conf keys: {}'.format(missing_in_sid_conf))
    else:
        log.info('\tOK: All FS keys are in sid_conf keys.')

    log.debug('done')


if __name__ == '__main__':

    log.debug('Starting')
    log.debug('Path Templates: ')
    for k, v in path_templates.items():
        log.info('{} -> {}'.format(k, v))

    log.debug('')
    log.debug('Tests:')
    test_fs_duplicates()
    test_missing()

    log.debug('Done')
