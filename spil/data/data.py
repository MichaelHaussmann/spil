from spil import Sid
from spil.sid.search.ss import SidSearch

from spil.util.log import debug, warning, error
from spil.conf import get_data_source as data_source, get_attribute_source as attribute_source
from spil.util.caching import lru_cache as cache


@cache
def get_data_source(sid):
    """
    For a given Sid, looks up the matching data_source, as given by config.
    Return value is an instance implementing SidSearch.

    Technical note: the result is cached.
    This means that the choice of the data source is cached, not the resulting data itself.
    The data source is called again each time a Data() method is called.
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        warning('Sid could not be created, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = data_source(_sid)
    if source:
        debug('Getting data source for "{}": -> {}'.format(sid, source))
        return source
    else:
        warning('Data Source not found for Sid "{}" ({})'.format(sid, _sid.type))
        return None


def get_attribute_source(sid, attribute):
    """
    For a given Sid and attribute, looks up the the matching data_source, as given by config.
    Return value is a callable (typically a function).
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        error('Sid could not be created, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = attribute_source(_sid, attribute)
    if source:
        debug('Getting attribute source for "{} / {}": -> {}'.format(sid, attribute, source))
        return source
    else:
        warning('Attribute Source not found for Sid "{} / {}" ({})'.format(sid, attribute, _sid.type))
        return None


def get(sid, attribute, do_cached=True):  # TODO: put the choice of caching or not in the data source config.
    if do_cached:
        return get_cached_attribute(sid, attribute)
    else:
        return get_attribute(sid, attribute)


def get_attribute(sid, attribute):
    source = get_attribute_source(sid, attribute)
    if source:
        return source(sid)

@cache
def get_cached_attribute(sid, attribute):
    source = get_attribute_source(sid, attribute)
    if source:
        return source(sid)


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

    sid = 'FTOT/A/PRP'
    sid = Sid(sid)
    value = get(sid, 'comment')
    print(value)

    def test(sid, limit=5):
        sid = Sid(sid)
        print(sid)
        got = Data().get(sid)
        if limit:
            print(list(got)[:limit])
        else:
            for i in got:
                print('"{}"'.format(i))
                value = get(i, 'comment')
                print(value)

    sids = ['CBM/*', 'CBM/*', 'CBM/A/*', 'FTOT/A/PRP/*']
    for sid in sids:
        test(sid, limit=None)
