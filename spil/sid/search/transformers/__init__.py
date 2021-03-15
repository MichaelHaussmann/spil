# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
Search Sid transformers

Each transformer takes a list of search sids strings, and returns a list of search sids strings.
"""

from spil.sid.search.transformers.expand import execute as expand
from spil.sid.search.transformers.extensions import execute as extensions
# from spil.sid.search.transformers.optional_key import execute as optional_key
from spil.sid.search.transformers.or_op import execute as or_op

# transformers by execution order for existing searches
list_search_transformers = [extensions, or_op, expand]


def transform(sid, transformers):
    """
    Takes the given sid string, executes transformers and returns a list of sid strings.
    :return:
    """
    previous = [str(sid)]
    for function in transformers:
        done = function(previous)
        previous = done
    result = previous

    result = list(set(result))  # keep sorting ?

    return sorted(result)


if __name__ == '__main__':

    from logging import FATAL
    from pprint import pprint
    from spil.util.log import setLevel, info

    info('Tests start')

    setLevel(FATAL)

    tests = [
        'aral/s/s010,s020/**/mb,nk,ma,img',
        'aral/i/**/valid/p/*/exr',
        'aral/i/**/p/0001/png',
        'aral/s/**/hou',
        'aral/i/**/p/*/exr,img, hou',
        'aral',
        'aral/a/**/img',
        'aral/c/s010/p010/animation/**/v001/p/vdb',
        'aral/s/s010/p010/comp/**/movie',
        'aral/i/s010/p010/**/exr'
    ]

    for test in tests:
        results = transform(test, list_search_transformers)
        print(test + '-->')
        pprint(results)

        print('*' * 10)

