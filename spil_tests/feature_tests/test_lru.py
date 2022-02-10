from spil.util.caching import lru_cache


def fib(n):
    if n in (1, 2):
        return 1
    else:
        return fib(n - 2) + fib(n - 1)

@lru_cache
def fib2(n):
    if n in (1, 2):
        return 1
    else:
        return fib2(n - 2) + fib2(n - 1)


from datetime import datetime


def time_fn(fn, *args):
    s = datetime.now()
    print(fn(*args))
    e = datetime.now()
    print(e - s)


if __name__ == '__main__':

    time_fn(fib, 40)
    time_fn(fib2, 40)