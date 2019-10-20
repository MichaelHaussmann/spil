# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

import os
import six

from spil.libs.util.log import debug, warn, info

from spil.libs.sid.sid import Sid

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path


class FS(object):
    """
    File System Layer.

    Uses the Path and Glob to find Sids on the Filesystem.

    Still experimental...

    # TODO : more tests...

    """

    @staticmethod
    def find(search_sid):

        search = Sid(search_sid)

        debug('Search : ' + str(search))

        path = search.path
        if not path:
            warn('Search sid {} did not resolve to a path. Cancelled.'.format(search))
            return

        debug('Search path : ' + str(path))

        project = Sid(search.project)
        project_path = project.path  # TODO need a way to find a root path depending on other sid parts (eg: fx caches)

        pattern = path.split(project_path + os.sep)[-1]

        debug('pattern : ' + str(pattern))
        debug('project_path : ' + str(project_path))

        if str(pattern) == str(project_path):
            warn('No valid search pattern')
            return

        found = Path(project_path).glob(pattern)  # TODO this is expensive (recursive) and limited to one project path.

        for path in found:
            yield Sid(path=path)

    @staticmethod
    def get_children(sid):
        sid = Sid(sid)  # make certain it is a Sid
        search_sid = sid + '*'
        if search_sid == sid:
            warn('Can not get children on a final sid.')
            return []
        return FS.find(search_sid)


if __name__ == '__main__':

    print('Tests are in tests.fx')
