
from spil.util.log import info, warning, debug

from spil.sid.core import sid_resolver
from spil.sid.core.uri_helper import apply_uri
from spil.sid.sid import Sid, DataSid


def sid_to_sid(sid: str = None) -> Sid:
    """
    Given sid is either a Sid object or a string.

    Builds a sid object and returns it.

    :return: Sid
    """
    debug(f'Starting with: {sid}')

    string = sid.full_string if isinstance(sid, Sid) else str(sid)

    if string.count('?'):  # sid contains URI ending. We put it aside, and later append it back
        string, uri = string.split('?', 1)
    else:
        uri = ''

    # resolving
    if string.count(':'):
        _type, string = string.split(':')
        _type, data = sid_resolver.sid_to_dict(string, _type)
    else:
        _type, data = sid_resolver.sid_to_dict(string)

    data_sid = DataSid()

    if not data:
        info(f'[Sid] Sid "{sid}" / {string} did not resolve to valid Sid data.')
        data_sid._init(string=string)
        return data_sid

    # no uri to handle, we return
    if not uri:
        data_sid._init(string=string, type=_type, data=data)
        return data_sid

    # applying the uri, and updating the type
    else:
        string, _type, data = apply_uri(string, uri=uri, type=_type, data=data)
        data_sid._init(string=string, type=_type, data=data)
        return data_sid


def data_to_sid(data: dict) -> Sid:

    # FIXME: when is this function used, and why don't we have the type at the same time ?

    # TODO: make a fast version when the data comes from an internal trusted and already typed call.

    debug(f'Starting with: {data}')

    _type = sid_resolver.dict_to_type(data)  # FIXME: terrible code
    if not _type:
        warning(f'[Sid] Data did not resolve to valid Sid type, returning empty Sid. Data: "{data}"')
        return DataSid()

    # Now getting sid and ordered dict
    sid = sid_resolver.dict_to_sid(data, _type)

    # TODO: this next line could be just a dict sorting ?
    type, data = sid_resolver.sid_to_dict(sid, _type)  # check if type == _type ?

    data = data or dict()

    data_sid = DataSid()
    data_sid._init(string=sid, type=_type, data=data)
    return data_sid


# @lru_kw_cache
def sid_factory(sid: str = None, data: dict = None) -> Sid:
    """
    Sid factory facade.
    Depending on input, calls a sid creation function and returns the produced sid.

    In case of multiple arguments, the first has priority (others are ignored).
    If no param is given, eg. Sid(), returns an empty Sid().

    :param sid: a Sid object or string
    :param data: a data dictionary
    :param path: a path for a Sid

    :return: Sid
    """
    debug(f"sid_factory start: {sid} - {data}")
    if sid:
        return sid_to_sid(sid)

    elif data:
        return data_to_sid(data=data)

    else:
        return DataSid()
