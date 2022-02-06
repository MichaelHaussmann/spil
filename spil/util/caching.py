"""
Thank you Hugh Brown
https://gist.github.com/hughdbrown

https://gist.github.com/hughdbrown/bf5c63792d5f912a162bf012fb6b4527

Also borrowed pieces from functool.py, Copyright (C) 2006-2013 Python Software Foundation

This is a minimal but fast lru implementation.

TODO: replace for PY3 with the functools.lru_cache implementation.
Note that the cache size needs to be high enough.

"""

from functools import wraps

_max_size = 4096*2*2  # approx 40 Mo


def lru_cache(user_function):
    cache = {}

    @wraps(user_function)
    def wrapper(*args):
        key = tuple(args)
        if key not in cache:
            # Validate we didn't exceed the max_size:
            if len(cache) >= _max_size:
                # Delete an item in the dict:
                # print('lru_cache over size')
                cache.popitem()  # does not make sens in PY2
                # cache.clear()
            cache[key] = user_function(*args)
        return cache[key]
    return wrapper


def lru_kw_cache(user_function):
    cache = {}

    @wraps(user_function)
    def wrapper(*args, **kwargs):
        key = tuple(args) + tuple(kwargs)
        if key not in cache:
            # Validate we didn't exceed the max_size:
            if len(cache) >= _max_size:
                # Delete an item in the dict:
                # print('lru_cache over size')
                cache.popitem()  # does not make sens in PY2
                # cache.clear()
            cache[key] = user_function(*args, **kwargs)
        return cache[key]

    def cache_clear():
        cache.clear()

    def cache_info():
        from pprint import pformat
        return pformat(cache)

    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info
    return wrapper

