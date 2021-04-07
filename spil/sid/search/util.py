"""
Code borrowed from the more-itertools project.
https://pypi.org/project/more-itertools/


https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#first

"""


def first(iterable, default=None):
    """Return the first item of *iterable*, or *default* if *iterable* is
    empty.

        >>> first([0, 1, 2, 3])
        0
        >>> first([], 'some default')
        'some default'

    :func:`first` is useful when you have a generator of expensive-to-retrieve
    values and want any arbitrary one. It is marginally shorter than
    ``next(iter(iterable), default)``.

    """
    try:
        return next(iter(iterable))
    except StopIteration as e:
        return default
