"""

This is the config file for data access.

It is ingested by spil.conf.data_conf_load, which reads it into spil.conf.


*This is beta / work in progress*

The data config specification is subject to change.
(without affecting spil's API).

"""
from __future__ import annotations
from pathlib import Path

#########################################################
# Path config
path_configs = {'local': 'spil_fs_conf',
                'server': 'spil_fs_server_conf'
                }
default_path_config = 'local'
#########################################################


#########################################################
# Config for FindInAll
def get_finder_for(search_sid, config=None):  # get finder by Sid and optional config
    """
    Configuration used by FindInAll, to define which Finder is used for a given Search Sid.

    For a given Search Sid, and optional config,
    looks up the Search Sid's type and the matching Finder, as defined in an ad-hoc dict.

    The "config" allows to create multiple FindInAll instances / behaviours.
    (similar to the FindInPaths where we Find in different file systems)

    Args:
        search_sid: sid that is searched by FindInAll
        config: optional config to be able to define multiple FindInAll instances.

    Returns:
        A Finder instance for this search.
    """
    # type: ignore
    from spil_sid_conf import projects, asset_types  # type: ignore
    from spil import FindInConstants, FindInPaths, Finder

    finder_paths = FindInPaths()
    finder_projects = FindInConstants("project", projects)
    finder_types = FindInConstants("type", ["a", "s"], parent_source=finder_projects)
    finder_assettypes = FindInConstants('assettype', asset_types, parent_source=finder_types)
    finder_asset_states = FindInConstants('state', ["w", "p"], parent_source=finder_paths)

    finders_by_type = {
        'project': finder_projects,
        'asset': finder_types,
        'shot': finder_types,
        'asset__assettype': finder_assettypes,
        'asset__state': finder_asset_states,
        'shot__state': finder_asset_states,
        'default': finder_paths
    }

    finder: Finder = finders_by_type.get(search_sid.type, {}) or finders_by_type.get('default', {})
    if finder:
        return finder
    else:
        return None


#########################################################
# Config for GetFromAll
def get_getter_for(sid, attribute=None, config=None):
    """
    Configuration used by GetFromAll, to define which Getter is used for a given Sid or Search Sid.

    For a given Sid, and optional attribute and config,
    looks up the Sid's type and the matching Getter, as defined in an ad-hoc dict.

    The "config" allows to create multiple GetFromAll instances / behaviours.
    (similar to the FindInPaths where we Get from different file systems)

    The function may return None, in which case the getter will not return anything.

    Args:
        sid: sid that is queried by GetFromAll
        attribute: optional attribute name
        config: optional config to be able to define multiple GetFromAll instances.

    Returns:
        A Getter instance for this search, or None is none is defined.
    """
    # from spil_action.libs.files import get_comment, get_size, get_time
    from spil import Getter, GetFromPaths
    # from spil_plugins.sg.get_sg import GetFromSG
    from hamlet_plugins.next_get import NextGetter

    attribute_getters = {
        "next.version": NextGetter()
        #'comment': get_comment,
        #'size': get_size,
        #'time': get_time,
    }

    getter: Getter | None = attribute_getters.get(attribute)
    if getter:
        return getter

    getters_by_type = {
        'project': None,
        'asset': None,
        'shot': None,
        'asset__assettype': None,
        'asset__state': None,
        'shot__state': None,
        # 'asset__asset': GetFromSG(),
        # 'shot__shot': GetFromSG(),
        # 'shot__sequence': GetFromSG(),
        # 'shot__task': GetFromSG(),
        # 'asset__task': GetFromSG(),
        'default': GetFromPaths()
    }

    if sid.type in getters_by_type:
        # getter can be explicitly None
        # in this case, no data can be retrieved.
        return getters_by_type.get(sid.type)
    else:
        return getters_by_type.get('default')


def get_writer_for(sid):
    """
    Configuration used by WriteToAll, to define which Writer is used for a given Sid.

    *This is work in progress*
    """
    raise NotImplementedError("get_writer_for is not implemented")


#########################################################
# Config for WriteToPaths & GetFromPaths
#
path_data_suffix = '.data.json'
# WriteToPath: create. If a template exists for a suffix (extension), we copy it.
create_file_using_template = {  # type: ignore
    # 'ma': '.../empty.ma',
    # 'mb': '.../empty.mb'
}
# WriteToPath: create. If no template exists, we create an empty file with path.touch(), if create_using_touch is True
create_file_using_touch = True
# If nothing of these is set, we do not create a file.


# Used by WriteToPaths and GetFromPaths
def get_data_json_path(sid_path: Path) -> Path:
    """
    For a given Sid path, returns the path of a hidden data "sidecar" json file.
    Adds a dot before the name and changes the extension to ".data.json"

    Args:
        sid_path: path of a Sid

    Returns:
        path of a hidden data sidecar json file.

    """

    # TODO: add file rotation
    data_path = sid_path.with_name('.' + sid_path.name).with_suffix(path_data_suffix)
    return data_path

# End of Config for WriteToPaths & GetFromPaths
#########################################################

