"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil.conf import extension_alias  # type: ignore # from sid conf
from spil.conf import sip, ors
from spil.sid.core import query_helper


def execute(sids):
    """
    Maps extension aliases to a list of "or operator" separated extensions.

    Examples (with comma "," being the or-operator) :
         img -> jpg,exr,dpx
         hou -> hip, hipnc
         maya -> ma, mb
    """
    result = []

    for sid in sids:
        result.append(extensions(sid))

    return result


def handle_extension(extension_string=""):
    """
    Updates the string representing the extension, by replacing the aliases by the actual extensions.

    Examples:
    >>> handle_extension('maya')
    'ma,mb'

    >>> handle_extension('maya, mov, mb')
    'ma,mb,mov'

    >>> handle_extension()
    ''
    """
    if not extension_string:
        return ""

    if extension_string.count(ors):
        extension_string = [x.strip() for x in extension_string.split(ors)]
    else:
        extension_string = [extension_string]

    result = []
    for ext in extension_string:
        ext = extension_alias.get(ext, [ext])
        result.extend(ext)

    return ",".join(sorted(list(set(result))))


def extensions(sid):
    """
    Replaces extension aliases in the given string.
    Does replacement on the main string, and on an optional query.

    Examples
    >>> extensions('bla/s/bla/bla/**/hou')
    'bla/s/bla/bla/**/hip,hipnc'

    >>> extensions('bla/s/bla/bla/**/exr?ext=maya, mov')
    'bla/s/bla/bla/**/exr?ext=ma,mb,mov'

    >>> extensions('bla/s/bla/bla/**/movie, ma?ext=maya, mov')
    'bla/s/bla/bla/**/avi,ma,mov,mp4?ext=ma,mb,mov'

    #FIXME: "ext" is hard coded.
    """

    sid = str(sid)

    if sid.count("?"):  # sid contains Query ending. We put it aside, and later append it back
        sid, query = sid.split("?", 1)
    else:
        query = ""

    # main sid
    parts = sid.split(sip)
    newsid = parts[:-1]  # SMELL: this might not be an extension at all. Still works.
    newsid.append(handle_extension(parts[-1]))

    # query part
    if query:
        query_dict = query_helper.to_dict(query)
        if query_dict.get("ext"):  # FIXME: "ext" is hard coded.
            query_dict["ext"] = handle_extension(query_dict.get("ext"))
        query = query_helper.to_string(query_dict)

    return sip.join(newsid) + ("?" + query if query else "")


if __name__ == "__main__":

    import doctest

    doctest.testmod()

    """
    from spil.util.log import setLevel, info
    from logging import FATAL
    info('Tests start')
    setLevel(FATAL)
    expandables = ['hamlet/s/*/hou',
                   'hamlet/s/*/p/*/exr,img, hou?test',
                   'hamlet',
                   'hamlet/a/*/img?test',
                   'hamlet/s/sq010/sh0010/anim/*/v001/p/vdb',
                   'hamlet/s/*/movie',
                   'hamlet/s/sq010/sh0010/**/exr?ext=maya, mov']

    for sid in expandables:
        print(sid + '-->' + str(extensions(sid)))
        print('*'*10)
    """
