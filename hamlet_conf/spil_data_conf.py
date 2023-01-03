"""

This is the config file for data access.

It is ingested by spil.conf.data_conf_load, which reads it into spil.conf.


*This is work in progress*

The data config specification is subject to change.
(without affecting spils API).

"""
# attribute getters
# cachable_attributes (by getter / by type / with TTL - for example publish file size, date, owner

# sid_cache_path = '/home/mh/PycharmProjects/spil2/hamlet_conf/data/caches'
# sid_cache_folder = sid_cache_path

# ---------------------------------------------
# Path config
path_configs = {'local': 'spil_fs_conf',
                'server': 'spil_fs_server_conf'
                }
default_path_config = 'local'

# WriteToPaths & GetFromPaths
path_data_suffix = '.data.json'
# WriteToPath: create. If a template exists for a suffix (extension), we copy it.
create_file_using_template = {  # type: ignore
    # 'ma': '.../empty.ma',
    # 'mb': '.../empty.mb'
}
# WriteToPath: create. If no template exists, we create an empty file with path.touch(), if create_using_touch is True
create_file_using_touch = True
# If nothing of these is set, we do not create a file.
# ---------------------------------------------
# End Path config


def get_finder_for(search_sid, config=None):  # get finder by Sid and optional config
    """
    Configuration used by FindInAll, to define which Finder is used for a given Search Sid.

    For a given Search Sid, and optional config,
    looks up the Search Sid's type and the matching Finder, as defined in an ad-hoc dict.

    The config allows to create multiple FindInAll instances / behaviours.
    (similar to the FindInPaths where we Find in different file systems)

    Args:
        search_sid: sid that is searched by FindInAll
        config: optional config to be able to define multiple FindInAll instances.

    Returns:
        A Finder object for this search.
    """
    # type: ignore
    from spil_sid_conf import projects, asset_types  # type: ignore
    from spil import FindInConstants, FindInPaths

    finder_projects = FindInConstants("project", projects)
    finder_types = FindInConstants("type", ["a", "s"], parent_source=finder_projects)
    finder_assettypes = FindInConstants('assettype', asset_types, parent_source=finder_types)

    finders_by_type = {
        'project': finder_projects,
        'asset__type': finder_types,
        'shot__type': finder_types,
        'asset__assettype': finder_assettypes,
        'default': FindInPaths()
    }

    finder = finders_by_type.get(search_sid.type, {}) or finders_by_type.get('default', {})
    if finder:
        return finder
    else:
        return None


def get_getter_for(sid, attribute):
    """

    *This is work in progress*

    For a given attribute, looks up the matching attribute_getters, as defined in a dict.
    Returned value is a getter function.

    Currently, the sid argument is not used.
    """
    # from spil_action.libs.files import get_comment, get_size, get_time

    attribute_getters = {
        #'comment': get_comment,
        #'size': get_size,
        #'time': get_time,
    }

    getter = attribute_getters.get(attribute)
    if getter:
        return getter
    else:
        print('No getter found for Attribute "{}" ({})'.format(attribute, sid))
        return None


def get_writer_for(sid):
    """
    *This is work in progress*
    """
    raise NotImplemented()

