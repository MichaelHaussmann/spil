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
    from sid_conf import projects, asset_types, asset_tasks, shot_tasks
    from spil.data.cs import CS
    from spil import FS

    # CS is for a Constant data source.
    cs_projects = CS('project', projects)
    cs_types = CS('type', ['a', 's'], parent_source=cs_projects)
    cs_assettypes = CS('assettype', asset_types, parent_source=cs_types)
    cs_asset_tasktypes = CS('tasktype', asset_tasks, parent_source= FS())
    cs_shot_tasktypes = CS('tasktype', shot_tasks, parent_source=FS())

    data_sources = {
        'project': cs_projects,
        'asset__type': cs_types,
        'shot__type': cs_types,
        'render__type': cs_types,
        'asset__assettype': cs_assettypes,
        'asset__tasktype': cs_asset_tasktypes,
        'shot__tasktype': cs_shot_tasktypes,
        'default': FS()
    }

    source = data_sources.get(sid.type, {}) or data_sources.get('default', {})
    #print('Sid {} --> {} --> {}'.format(sid.full_string, sid.type, source))
    if source:
        return source
    else:
        #print('Data Source not found for Sid "{}" ({})'.format(sid, sid.type))
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
