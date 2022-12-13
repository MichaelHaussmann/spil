from spil import Sid
from spil import conf
from spil.util.caching import lru_cache as cache


class Getter:
    pass


def get(sid, attribute, do_cached=True):  # TODO: put the choice of caching or not in the data source config_name.
    if do_cached:
        return get_cached_attribute(sid, attribute)
    else:
        return get_attribute(sid, attribute)


def get_attribute_source(sid, attribute):
    """
    For a given Sid and attribute, looks up the matching data_source, as given by config_name.
    Return value is a callable (typically a function).
    """
    _sid = Sid(sid)
    if not str(_sid) == str(sid):
        error('Sid could not be created, this is likely a configuration error. "{}" -> {}'.format(sid, _sid))
    source = conf.get_attribute_source(_sid, attribute)
    if source:
        debug('Getting attribute source for "{} / {}": -> {}'.format(sid, attribute, source))
        return source
    else:
        warning('Attribute Source not found for Sid "{} / {}" ({})'.format(sid, attribute, _sid.type))
        return None


def get_attribute(sid, attribute):
    source = get_attribute_source(sid, attribute)
    if source:
        return source(sid)


@cache
def get_cached_attribute(sid, attribute):
    source = conf.get_attribute_source(sid, attribute)
    if source:
        return source(sid)


def reload_data_source(sid):
    """
    Reloads the data source for given sid
    """
