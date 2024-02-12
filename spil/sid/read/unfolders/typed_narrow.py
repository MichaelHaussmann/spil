"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil import Sid
from spil.conf import basetyped_search_narrowing, typed_search_narrowing  # type: ignore


def execute(sids):
    """
    Once a search Sid is typed, we may need to narrow down the values,
    (filling the string with values)
    to make sure the right type is hit in the search.

    The transformation cannot yet be properly automated.
    For that reason it is set in a config_name, and handled here.

    TODO: for more precise results we might want to implement this on types also,
    not only basetypes.

    Examples:
        >>> type_narrow(Sid("asset__assettype:hamlet/*/*"))
        Sid('asset__assettype:hamlet/a/*')

        >>> type_narrow(Sid("shot__sequence:hamlet/*/*"))
        Sid('shot__sequence:hamlet/s/*')

    Args:
        sids:

    Returns:

    """
    result = []

    for sid in sids:
        result.append(type_narrow(sid))

    return result


def type_narrow(sid: Sid) -> Sid:
    """
    For a sids basetype, then type, looks up the configured query, and applies it.

    Args:
        sid:

    Returns:
        sid with applied configured queries
    """

    query = basetyped_search_narrowing.get(sid.basetype, "")
    if query:
        sid = sid.get_with(query=query)
    query = typed_search_narrowing.get(sid.type, "")
    if query:
        sid = sid.get_with(query=query)
    return sid


if __name__ == "__main__":

    from spil.util.log import DEBUG, setLevel, INFO

    # import doctest
    # doctest.testmod()
    setLevel(INFO)
    # sid = Sid("asset__assettype:hamlet/a/char")
    sid = Sid("asset__file:hamlet/a/char/hamlet/model/v001/p/*")
    s = type_narrow(sid)
    print(s.uri)

    sid = Sid("asset__movie_file:hamlet/a/char/hamlet/model/v001/p/*?type=~a")
    s = type_narrow(sid)
    print(s.uri)

    sids = [
        Sid("asset__file:hamlet/a/char/hamlet/model/v001/p/*"),
        Sid("asset__movie_file:hamlet/a/char/hamlet/model/v001/p/*"),
        Sid("asset__cache_file:hamlet/a/char/hamlet/model/v001/p/*"),
    ]

    done = execute(sids)
    print(done)
