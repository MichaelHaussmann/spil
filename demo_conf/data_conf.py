from spil.data.sid_cache import SidCache


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

from spil import LS, FS

data_sources = {
    'project': SidCache,  # TODO: as string, than import on the fly, not import here
    'asset': SidCache,
    'shot': SidCache,
    'default': FS
}
