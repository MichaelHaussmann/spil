
# attribute getters
# cachable_attributes (by getter / by type / with TTL - for example publish file size, date, owner


sid_cache_path = '/home/mh/PycharmProjects/spil2/hamlet_conf/data/caches'
sid_cache_folder = sid_cache_path

path_configs = {'local': 'fs_conf',
                'server': 'fs_server_conf'
                }

default_path_config = 'local'

# WriteToPath: create
# When a Sid that has a suffix (an extension), we want to create a file.
# If a template exists for the suffix, we copy it.
create_file_using_template = {
    'ma': '/home/mh/PycharmProjects/spil2/hamlet_conf/data/templates/empty.ma',
    'mb': '/home/mh/PycharmProjects/spil2/hamlet_conf/data/templates/empty.mb'
}
# if no template exists, we create an empty file with path.touch(), if create_using_touch is True
create_file_using_touch = True
# If nothing of these is set, we do not create a file.


def get_finder_for(sid):  # get finder by type
    """
    For a given Sid, looks up the Sid type and the matching data_source, as defined in a dict.
    Returned value from the config_name is an instance.
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


def get_getter_for(sid, attribute):
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

def get_writer_for(sid):
    pass