# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil import Sid
from spil.util.exception import SpilException
from spil.sid.search.ss import SidSearch

from spil.util.log import debug


class CS(SidSearch):
    """
    Config / Constant Sid Source.

    Implements star_search for a specific key, by getting the values from a given, constant, list.
    If there is a search "above" the given key, the search is delegated to the given "parent_source".

    This is used to create a Data Source for constant values.

    Example:
        ```
        >>> fs = FS()
        >>> cat_cs = CS('cat', ['characters', 'props', 'sets'], parent_source=fs)
        >>> list( cat_cs.get('hamlet/s/*') )
        # gets: [Sid('hamlet/s/characters'), Sid('hamlet/s/props'), Sid('hamlet/s/sets')]
        ```

    Still alpha.
    """

    def __init__(self, key, values, parent_source=None):
        self.key = key
        self.values = values
        self.parent_source = parent_source

    def _append_value(self, root, done, as_sid=False):

        for value in self.values:

            result = root.get_with(key=self.key, value=value)
            if not result:
                debug(
                    'Generated Sid "{}" is not valid, skipped (built {} with {}:{})'.format(
                        result, result, self.key, value
                    )
                )
                continue

            if result not in done:
                done.add(result)
                if as_sid:
                    yield result
                else:
                    yield str(result)

    def star_search(self, search_sids, as_sid=False, do_sort=False):

        done = set()

        for search_sid in search_sids:

            root = Sid(search_sid).get_as(self.key)

            if "*" not in str(root):

                if as_sid:
                    yield root
                else:
                    yield str(root)

            elif "*" in str(root.parent) and root != root.parent:

                if not self.parent_source:
                    raise SpilException(
                        "The parent of {} is itself a search, but no parent_source was given.".format(
                            root
                        )
                    )

                for found_root in self.parent_source.get(root):
                    generator = self._append_value(found_root, done, as_sid=as_sid)
                    for i in generator:
                        yield i
            else:

                generator = self._append_value(root, done, as_sid=as_sid)
                for i in generator:
                    yield i


if __name__ == "__main__":

    from sid_conf import projects
    from spil.util.log import setLevel, ERROR, DEBUG, WARN, INFO

    setLevel(ERROR)

    cs1 = CS("project", projects)
    cs2 = CS("type", ["A", "R", "S"], parent_source=cs1)
    print(cs2)

    for i in cs1.get("*"):
        print(i)
        print(i.path)

    for i in cs2.get("FTOT/*"):
        print(i)
        print(i.path)
