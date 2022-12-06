# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.conf import basetyped_search_narrowing


def execute(sids):
    """
    Once a search Sid is typed, we may need to narrow down the values, to make sure the right type is hit in the search.

    For example:
    "asset_cat:hamlet/*/*" and "shot_seq:hamlet/*/*"
    should be narrowed down to
    "asset_cat:hamlet/a/*" and "shot_seq:hamlet/s/*"

    The transformation cannot yet be properly automated.
    For that reason it is set in a config, and handled here.

    """
    result = []

    for sid in sids:
        result.append(type_narrow(sid))

    return result


def type_narrow(sid):

    uri = basetyped_search_narrowing.get(sid.basetype, '')
    if uri:
        sid = sid.get_with(uri=uri)
    return sid


if __name__ == '__main__':

    import doctest
    doctest.testmod()


