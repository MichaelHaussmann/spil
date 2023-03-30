# TODO: put keys in official ENUM
from enum import Enum

from spil import FindInAll
from spil.sid.pathops.pathconfig import PathConfig
from spil.util.caching import lru_cache as cache

context_keys = Enum


@cache
def get_context(name: str):
    """
    get a Context object, containing "sid_finder", etc.
    """
    pass


def set_context(name: str):
    """
    set env variables - like current context
    """
    pass

"""
"context immutable":
sid, fs confs, are imported on startup



context = {}

context["local"] = {
    "name": "local",
    # "sid_path_config": "local",
    "sid_finder": FindInAll(),
    "sid_getter": GetFromAll(),
    "sid_path_config": "local",
    "default_path_config": "local",
}

last_used_context = None
current_used_context = "local"
"""