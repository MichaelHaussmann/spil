# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
"""
Data config example for the Spil data framework.

For any given Sid, finds the Data Source that is to be used, and returns an instance or function.

Note: imports are in the function to avoid circular import limitations at boot.
"""


def get_data_source(sid):
    """
    For a given Sid, looks up the Sid type and the matching data_source, as defined in a dict.
    Returned value from the config is an instance.
    """
    from spil.data.sid_cache import SidCache
    from spil import FS

    sid_cache_file = '..../data/sid_caches/all.sids.txt'
    sid_cache_instance = SidCache(sid_cache_file)  # is a Singleton

    data_sources = {
        'project': sid_cache_instance,
        'asset': sid_cache_instance,
        'asset__cat': sid_cache_instance,
        'shot__seq': sid_cache_instance,
        'shot': sid_cache_instance,
        'default': FS()
    }

    source = data_sources.get(sid.type, {}) or data_sources.get('default', {})
    if source:
        return source
    else:
        print('Data Source not found for Sid "{}" ({})'.format(sid, sid.type))
        return None


def get_attribute_source(sid, attribute):
    """
    For a given attribute, looks up the matching attribute_sources, as defined in a dict.
    Returned value is a function.

    Currently the sid argument is not used.
    """
    # from pipe_action.libs.files import get_comment, get_size, get_time

    attribute_sources = {
        #'comment': get_comment,
        #'size': get_size,
        #'time': get_time,
    }

    source = attribute_sources.get(attribute)
    if source:
        return source
    else:
        print('Attribute Source not found for Attribute "{}" ({})'.format(attribute, sid))
        return None
