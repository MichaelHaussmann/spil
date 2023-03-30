# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
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

_max_size = 4096 * 2 * 2  # approx 40 Mo
_max_size = 4096


def lru_cache(user_function):
    cache = {}

    @wraps(user_function)
    def wrapper(*args):
        key = tuple(args)
        if key not in cache:
            # Validate we didn't exceed the max_size:
            if len(cache) >= _max_size:
                cache.popitem()
                # cache.clear()
            cache[key] = user_function(*args)
        return cache[key]

    def cache_clear():
        cache.clear()

    def cache_info():
        from pprint import pformat
        return pformat(cache)

    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info

    return wrapper


def lru_kw_cache(user_function):
    cache = {}
    #stats = [0, 0]  # hits,misses

    @wraps(user_function)
    def wrapper(*args, **kwargs):
        #return user_function(*args, **kwargs)
        key = tuple(args) + tuple(kwargs)
        if key not in cache:
            #stats[1] += 1  # miss
            # Validate we didn't exceed the max_size:
            if len(cache) >= _max_size:
                cache.popitem()
                # cache.clear()
            cache[key] = user_function(*args, **kwargs)
        else:
            #stats[0] += 1  # hit
            pass
        return cache[key]

    def cache_clear():
        cache.clear()
        #stats[0] = stats[1] = 0

    def cache_info():
        from pprint import pformat
        return pformat(cache)
        #return f"Hits: {stats[0]}/ Misses: {stats[1]} / Cache: {pformat(cache)}"

    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info
    return wrapper


def hit_cache(user_function):
    """
    A cache decorator that caches only if the wrapped function returns something.
    This is useful on data that is often queried but rarely or not at all erased.

    TODO: add TTL mechanism

    Args:
        user_function:

    Returns:

    """
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
            returned = user_function(*args, **kwargs)
            if returned:
                cache[key] = returned
            else:
                return returned
        return cache[key]

    def cache_clear():
        cache.clear()

    def cache_info():
        from pprint import pformat
        return pformat(cache)

    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info
    return wrapper



