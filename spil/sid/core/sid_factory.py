from __future__ import annotations
from typing import Optional
import os

from spil.sid.sid import Sid

from spil.util.log import info, warning, debug
from spil.sid.core import sid_resolver
from spil.sid.core.uri_helper import apply_uri
from spil.sid.pathops import fs_resolver


def sid_to_sid(sid: Optional[str] = None) -> Sid:
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
        _type, fields = sid_resolver.sid_to_dict(string, _type)
    else:
        _type, fields = sid_resolver.sid_to_dict(string)

    new_sid = Sid(from_factory=True)

    if not fields:
        info(f'[Sid] Sid "{sid}" / {string} did not resolve to valid Sid fields.')
        new_sid._init(string=string)
        return new_sid

    # no uri to handle, we return
    if not uri:
        new_sid._init(string=string, type=_type, fields=fields)
        return new_sid

    # applying the uri, and updating the type
    else:
        string, _type, fields = apply_uri(string, uri=uri, type=_type, fields=fields)
        new_sid._init(string=string, type=_type, fields=fields)
        return new_sid


def dict_to_sid(fields: dict) -> Sid | None:

    # FIXME: when is this function used, and why don't we have the type at the same time ?

    # TODO: make a fast version when the fields comes from an internal trusted and already typed call.

    debug(f'Starting with: {fields}')

    _type = sid_resolver.dict_to_type(fields)  # FIXME: terrible code
    if not _type:
        warning(f'Fields did not resolve to valid Sid type, returning empty Sid. fields: "{fields}"')
        return None

    # Now getting sid and ordered dict
    sid = sid_resolver.dict_to_sid(fields, _type)

    # TODO: this next line could be just a dict sorting ?
    type, fields = sid_resolver.sid_to_dict(sid, _type)  # check if type == _type ?

    if not fields:
        warning(f'After resolving back from Sid {sid}, Fields are empty. Your should investigate the config_name. Returning empty Sid.')
        return None

    new_sid = Sid(from_factory=True)
    new_sid._init(string=sid, type=_type, fields=fields)
    return new_sid


def path_to_sid(path: str | os.Pathlike[str], config: str | None) -> Sid | None:

    # resolving
    _type, fields = fs_resolver.path_to_dict(path, config=config)

    if not fields:
        info(f"Path [{path}] did not resolve to valid Sid fields (config_name:{config}.")
        return None

    # Now getting sid
    resolved_sid = sid_resolver.dict_to_sid(fields, _type)
    if not resolved_sid:
        info('Path "{}" did resolve to fields {}, but not back to Sid'.format(path, fields))
        return None

    new_sid = Sid(from_factory=True)
    new_sid._init(string=resolved_sid, type=_type, fields=fields)
    return new_sid


# @lru_kw_cache
def sid_factory(sid: Optional[str] = None,
                fields: dict = None,
                path: os.Pathlike[str] | str | None = None,
                config: Optional[str] = None) -> Sid:
    """
    Sid factory facade.
    Depending on input, calls a sid creation function and returns the produced sid.

    In case of multiple arguments, the first has priority (others are ignored).
    If no param is given, eg. Sid(), returns an empty Sid().

    Important:
    Python always calls __init__ on objects returned by __new__.
    In this factory, we circumvent doubled __init__ calls, by having an empty __init__, and calling an explicit _init() method.
    To implement a new factory method, it is needed to explicitely call this _init(), or the DataSid object will end up malformed.

    :param sid: a Sid object or string
    :param fields: a fields dictionary
    :param path: a path for a Sid
    :param config: config_name name for the path resolving

    :return: Sid
    """
    debug(f"sid_factory start: {sid} - {fields} - {path}")
    result = None
    if sid:
        result = sid_to_sid(sid)

    elif fields:
        result = dict_to_sid(fields=fields)

    elif path:
        result = path_to_sid(path=path, config=config)

    if result is not None:
        return result
    else:
        new_sid = Sid(from_factory=True)
        new_sid._init()
        return new_sid
