# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import itertools as it

import os
import six
import glob

from spil import conf
from spil.sid.search.ss import SidSearch
from spil.sid.sid import Sid
from spil.util.exception import SpilException
from spil.util.log import debug, warn, info


class FS(SidSearch):
    """
    File search.

    Searches for sids in a File System.

    Still experimental.

    """

    #def exists(self, search_sid):  TODO: Test and compare with SidSearch.exists
    #    return os.path.exists(search_sid.path)

    def star_search(self, search_sids, as_sid=False, do_sort=False):
        """
        Simple star search.

        Uses Glob.

        :param search_sids:
        :param as_sid:
        :param do_sort:
        :return:
        """
        if do_sort:
            info('do_sort not implemented in FS')

        done = set()
        done_add = done.add  # performance

        for search_sid in search_sids:

            debug('[fs_star_search] "{}"'.format(search_sid))

            search = search_sid  # TODO: handle also strings ?

            debug('Search : ' + str(search))
            debug('PATH : {}'.format(search.path))
            path = search.path

            if not path:
                warn('Search sid {} did not resolve to a path. Cancelled.'.format(search))
                return

            debug('Search path : ' + str(path))

            # TODO need a way to find a root path depending on other sid parts (eg: fx caches)
            project_path = search.get_as('project').path

            pattern = path.split(project_path + '/')[-1]

            for key, value in six.iteritems(conf.search_path_mapping):
                pattern = pattern.replace(key, value)

            debug('pattern : ' + str(pattern))
            debug('project_path : ' + str(project_path))

            found = glob.glob(os.path.join(project_path, pattern))
            debug('found')
            debug(found)
            for path in found:
                path = str(path).replace(os.sep, '/')
                try:
                    sid = Sid(path=path)
                    debug('found ' + str(sid))
                except SpilException as e:
                    debug('Path did not generate sid : {}'.format(path))
                    continue
                if not sid:
                    warn('Path did not generate sid : {}'.format(path))
                    continue

                item = str(sid)
                if item not in done:
                    done_add(item)
                    if as_sid:
                        yield sid
                    else:
                        yield item
                else:
                    debug('{} was already found, skipped. '.format(item))


if __name__ == '__main__':

    pass
