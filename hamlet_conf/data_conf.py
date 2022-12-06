
# attribute getters
# cachable_attributes (by getter / by type / with TTL - for example publish file size, date, owner


sid_cache_path = '/home/mh/PycharmProjects/spil2/hamlet_conf/data/templates'


path_configs = {'local': 'fs_conf',
                'server': 'fs_server_conf'
                }

default_path_config = 'local'

# WriteToPath: create
# When a Sid that has a suffix (an extension), we want to create a file.
# If a template exists for the suffix, we copy it.
create_file_using_template = {
    'ma': '/home/mh/PycharmProjects/spil2/hamlet_conf/data/empty.ma',
    'mb': '/home/mh/PycharmProjects/spil2/hamlet_conf/data/empty.mb'
}
# if no template exists, we create an empty file with path.touch(), if create_using_touch is True
create_file_using_touch = True
# If nothing of these is set, we do not create a file.
