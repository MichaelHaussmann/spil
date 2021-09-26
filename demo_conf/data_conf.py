# THIS IS WORK IN PROGRESS.

"""
WOrk in progress
def file_get_comment(sid):
    return 'Cool Comment for ' + str(sid)
    # comment = readlines


implementations = {
    'next_version': {
        'shot__file': ''
    },
    'comment': {
        'shot__file': file_get_comment,
        'asset__file': file_get_comment,
        'asset__movie_file': file_get_comment,
        'shot__movie_file': file_get_comment,
    },
}
"""

def get_data_source(sid):
    """
    For a given Sid, looks up the Sid type and the matching data_source, as defined in config.
    Return value from the config is an instance.
    """
    from spil.data.sid_cache import SidCache
    from spil import FS

    sid_cache_file = 'V:/TESTPREMIERE/sids.test.txt'
    sid_cache_instance = SidCache(sid_cache_file)

    data_sources = {
        'project': sid_cache_instance,
        # IDEA: as string, than import on the fly, not import here ? who gets to control instancing
        'asset': sid_cache_instance,
        'asset__cat': sid_cache_instance,
        'shot__seq': sid_cache_instance,
        'shot': sid_cache_instance,
        'default': FS()
    }

    # sid = Sid(sid)
    source = data_sources.get(sid.type, {}) or data_sources.get('default', {})
    if source:
        return source
    else:
        print('Data Source not found for Sid "{}" ({})'.format(sid, sid.type))
        return None