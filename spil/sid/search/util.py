# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.util.log import debug

"""
Code borrowed from the more-itertools project.
https://pypi.org/project/more-itertools/


https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#first

"""
from spil import Sid


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


def extrapolate(sids, as_sid=False):
    """
    From an iterable containing leaf node paths, extrapolates all the subnode paths.

    This is useful when the data source quickly provides leaves only, but we want to find child data.

    For example: the path "TEST/A/CHR/HERO/MOD/V001/W/avi"
    will generate: "TEST/A/CHR/HERO/MOD/V001/W", "TEST/A/CHR/HERO/MOD/V001", "TEST/A/CHR/HERO/MOD", etc.
    until "TEST"

    :param sids: generator
    :return:
    """

    debug("Start Extrapolate {}".format(sids))  # TODO: warning if a string or Sid is given, need iterable.

    generated = set()

    for sid in sids:

        generated.add(sid)
        # print(sid)
        yield sid

        parts = str(sid).split("/")
        for i, key in enumerate(reversed(parts[:-1]), 1):
            new_sid = "/".join(parts[: -1 * i])
            if new_sid in generated:
                break
            else:
                generated.add(new_sid)
                # print(new_sid)
                if as_sid:
                    yield Sid(new_sid)
                else:
                    yield new_sid
