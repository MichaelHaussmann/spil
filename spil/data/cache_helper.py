from spil.data.data import get_cached_attribute


# FIXME: this is work in progress


def reload_lru_caches():
    """
    Reloads all current lru caches.


    """
    from spil.sid.core.sid_resolver import sid_to_dict
    from spil.sid.core.fs_resolver import path_to_dict

    cached_functions = [get_cached_attribute(), sid_to_dict, path_to_dict]
    for f in cached_functions:
        f.cache_clear()
