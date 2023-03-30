"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from typing import List

from spil.conf import sip, ors
from spil.sid.core import query_helper


def execute(sids: List[str]) -> List[str]:
    """
    Runs or_op (the "or operator") on a list of Sids.

    Args:
        sids: a list of Sid strings to edit

    Returns: the list of Sid strings, edited
    """
    result = []
    for sid in sids:
        result.extend(or_op(sid))

    return result


def or_op(sid: str) -> List[str]:
    """
    or_op (the "or operator") transforms a string containing the "or" sign
    into a list of strings, each one individually representing the options without the or.

    Note: the ors sign can be configured, it is called "ors" in the config.
    Typically it is a comma ",".

    Example:

        >>> or_op('bla/s/bla/A,B/**/one,two?test=X,Y,Z')
        ['bla/s/bla/A/**/one?test=X', 'bla/s/bla/A/**/one?test=Y', 'bla/s/bla/A/**/one?test=Z', 'bla/s/bla/B/**/one?test=X', 'bla/s/bla/B/**/one?test=Y', 'bla/s/bla/B/**/one?test=Z', 'bla/s/bla/A/**/two?test=X', 'bla/s/bla/A/**/two?test=Y', 'bla/s/bla/A/**/two?test=Z', 'bla/s/bla/B/**/two?test=X', 'bla/s/bla/B/**/two?test=Y', 'bla/s/bla/B/**/two?test=Z']

    Args:
        sid: a sid string

    Returns: a list of Sid strings
    """
    sid = str(sid)
    if not sid.count(ors):  # no "or" operators in sid.
        return [sid]

    if sid.count("?"):  # sid contains Query ending. We put it aside, and later append it back
        sid, query = sid.split("?", 1)
    else:
        query = ""

    sids = or_on_path(sid)

    result = []
    if query:
        uris = or_on_query(query)
        for s in sids:
            for u in uris:
                result.append("{}?{}".format(s, u))
    else:
        result = sids

    return result


def or_on_path(sid):
    """
    Applies the or_op on the path part of the Sid.

    Example:

        >>> or_on_path('bla/s/bla/A,B,C/**/one,two,three')
        ['bla/s/bla/A/**/one', 'bla/s/bla/B/**/one', 'bla/s/bla/C/**/one', 'bla/s/bla/A/**/two', 'bla/s/bla/B/**/two', 'bla/s/bla/C/**/two', 'bla/s/bla/A/**/three', 'bla/s/bla/B/**/three', 'bla/s/bla/C/**/three']

    Args:
        sid: sid string

    Returns: list of sid string
    """

    _start = "--start--"

    parts = sid.split(sip)

    found = [_start]
    for part in parts:
        current = found.copy()
        if ors in part:
            for alt in part.split(ors):
                alt = alt.strip()
                for sid in current.copy():
                    new = sid + sip + alt
                    # print 'replace', sid, ' --> ', new, ' -- ', sid in found, '?'
                    #
                    if sid in found:
                        found[found.index(sid)] = new  # replace (of the first element)
                    else:
                        found.append(new)  # replace (of the first element)

            # found.remove()
        else:
            for sid in found.copy():
                new = sid + sip + part
                # print new
                found[found.index(sid)] = new  # replace (of the first element)

    result = []
    for sid in found:
        if not sid in result:
            result.append(sid.replace(_start + sip, ""))

    # no type check needed
    return result


def or_on_query(query):
    """
    Applies the or operator to values of the query, creating unique uris without the operator.

    Example:

        >>> or_on_query('titi=tata,blip&roger=vadim,bom,tom, tata')
        ['titi=tata&roger=vadim', 'titi=blip&roger=vadim', 'titi=tata&roger=bom', 'titi=blip&roger=bom', 'titi=tata&roger=tom', 'titi=blip&roger=tom', 'titi=tata&roger=tata', 'titi=blip&roger=tata']

    Args:
        query:

    Returns:

    """
    query_dict = query_helper.to_dict(query)
    result = [query_dict.copy()]
    for key, value in query_dict.items():
        if value.count(ors):
            new_result = []
            for i in value.split(ors):
                for d in result.copy():
                    new_dict = d.copy()
                    new_dict[key] = i
                    new_result.append(new_dict)
            result = new_result
    #     print(result)

    return [query_helper.to_string(d) for d in result]


if __name__ == "__main__":

    import doctest

    doctest.testmod()
