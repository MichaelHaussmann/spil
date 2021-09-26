from spil import Sid
from spil.sid.search.ss import SidSearch

from spil.util.log import debug, warning, error
from spil.conf import get_data_source as data_source
from spil.vendor.py2_lru import lru_cache as cache


@cache
def get_data_source(sid):
    """
    For a given Sid, looks up the Sid type and the matching data_source, as defined in config.
    Return value from the config is an instance.
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        error('Sid could not be created, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = data_source(_sid)
    if source:
        debug('Getting source for "{}": -> {}'.format(sid, source))
        return source
    else:
        warning('Data Source not found for Sid "{}" ({})'.format(sid, _sid.type))
        return None


class Data(SidSearch):
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    def get(self, search_sid, as_sid=True):
        source = get_data_source(search_sid)
        if source:
            return source.get(search_sid, as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        source = get_data_source(search_sid)
        if source:
            return source.get_one(search_sid, as_sid=as_sid)

    def exists(self, search_sid):
        source = get_data_source(search_sid)
        if source:
            return source.exists(search_sid)


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, ERROR

    setLevel(ERROR)

    def test(sid, limit=5):
        sid = Sid(sid)
        print(sid)
        got = Data().get(sid)
        if limit:
            print(list(got)[:limit])
        else:
            for i in got:
                print('"{}"'.format(i))

    sids = ['CBM/*', 'CBM/*', 'CBM/A/*', 'FTOT/A/PRP/*']
    for sid in sids:
        test(sid)
