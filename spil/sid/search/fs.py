# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

import os
import six
import glob

from spil import conf
from spil.sid.search.ss import SidSearch
from spil.sid.sid import Sid
from spil.util.exception import SpilException
from spil.util.log import debug, warn, info, error

try:
    import fileseq
except:
    fileseq = None
    error('fileseq could not be imported. File sequence search will not work.')

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
        Star search main function.

        Delegates to star_search_simple, or to star_search_framed to handle file sequences, if "frame=*" is in the search

        :param search_sids:
        :param as_sid:
        :param do_sort:
        :return:
        """
        if do_sort:
            info('do_sort not implemented in FS')

        # depending on input, select the right generator
        is_framed_search = any([ssid.get('frame') == '*' for ssid in search_sids])  #FIXME: hardcoded "frame"

        if is_framed_search and fileseq:
            generator = self.star_search_framed(search_sids, as_sid=as_sid)
        else:
            generator = self.star_search_simple(search_sids, as_sid=as_sid)

        for i in generator:
            yield i

    def star_search_simple(self, search_sids, as_sid=False):
        """
        Simple star search.

        Uses Glob.

        :param search_sids:
        :param as_sid:
        :return:
        """
        debug('Starting star_search_simple')

        done = set()
        done_add = done.add  # performance

        for search_sid in search_sids:

            debug('[fs_star_search] "{}"'.format(search_sid))

            search = search_sid  # TODO: handle also strings ?

            debug('Search : ' + str(search))
            pattern = search.path

            if not pattern:
                warn('Search sid {} did not resolve to a path. Cancelled.'.format(search))
                return

            for key, value in six.iteritems(conf.search_path_mapping):
                pattern = pattern.replace(key, value)

            debug('Search pattern : ' + str(pattern))

            found = glob.glob(pattern)
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

    def star_search_framed(self, search_sids, as_sid=False):
        """
        Star search with file sequence handling.

        Uses Glob and fileseq.

        :param search_sids:
        :param as_sid:
        :return:
        """
        debug('Starting star_search_framed')

        done = set()
        done_add = done.add  # performance

        for search_sid in search_sids:

            debug('[fs_star_search] "{}"'.format(search_sid))

            search = search_sid  # TODO: handle also strings ?

            if search.get('frame') == '*':  #FIXME: hardcoded "frame"
                search = search.get_with('frame', '@')  # for usage in fileseq

            debug('Search : ' + str(search))
            pattern = search.path

            if not pattern:
                warn('Search sid {} did not resolve to a path. Cancelled.'.format(search))
                return

            for key, value in six.iteritems(conf.search_path_mapping):
                pattern = pattern.replace(key, value)

            dir_pattern, file_pattern = os.path.split(pattern)
            debug(dir_pattern)
            parents = glob.glob(dir_pattern)
            file_sequences = []
            for parent in parents:
                file_search = os.path.join(parent, file_pattern).replace(os.sep, '/')
                debug('search ' + file_search)
                file_sequences.extend(fileseq.findSequencesOnDisk(file_search))

            debug('found sequences : {}'.format(file_sequences))
            for file_sequence in file_sequences:
                debug(file_sequence)
                path = str(file_sequence[0]).replace(os.sep, '/')  # we get the first file of the sequence
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
