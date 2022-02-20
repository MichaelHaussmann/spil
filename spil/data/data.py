"""

- optional: deactivate lru caching (for performance tests)

NOTE: searches where the type is followed by a /** ('FTOT/*/**') are currently unsupported due to faulty expand script.
Performances of FS: 100 sids per second, 1000 per second after memory caching.
"""

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
        warning('Sid could not be instanced, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = data_source(_sid)
    if source:
        debug('Getting data source for "{}": -> {}'.format(sid, source))
        return source
    else:
        warning('Data Source not found for Sid "{}" ({})'.format(sid, _sid.type))
        return None


def get_data_destination(sid):  # TODO: implement separate source and destination objects.
    return get_data_source(sid)


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


def reload_data_source(sid):
    """
    Reloads the data source for given sid
    """


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, ERROR

    setLevel(ERROR)
