"""
Thank you Hugh Brown
https://gist.github.com/hughdbrown

https://gist.github.com/hughdbrown/bf5c63792d5f912a162bf012fb6b4527

This is a minimal but fast lru implementation.

TODO: replace for PY3 with the functools.lru_cache implementation.
Note that the cache size needs to be high enough.

"""

from functools import wraps

_max_size = 4096


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
                cache.popitem()
            cache[key] = user_function(*args)
        return cache[key]
    return wrapper


