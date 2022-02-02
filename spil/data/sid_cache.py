from spil import Sid
from spil.util.pool import Pooled

from spil.util.log import debug
from spil.sid.search.util import first
from spil.sid.search.ls import LS
from spil.sid.search.ss import SidSearch

import six
if six.PY2: from pathlib2 import Path   # noqa
else: from pathlib import Path          # noqa


class SidCache(SidSearch, Pooled):
    """
    Simple Sid cache implementation, using LS ListSearch with a file.

    This class is "Pooled" :
        Each sid_cache_file is handled by its own, single, SidCache instance.
        A SidCache object handles only one sid_cache_file.
        For example:
            a = SidCache(sid_cache_file='/shots.txt')
            b = SidCache(sid_cache_file='/shots.txt')
            c = SidCache(sid_cache_file='/assets.txt')
            a and b will be the same object instance, and access the same data.
            c will be another object.
    Note that the file can be accessed concurrently from different python instances, from different machines.
    SidCache still needs to assure threadsafety.

    TODO: file create/update.
    TODO: cache reload from file, using file date (make self.cache_list into function that checks for file time, and updates list if needed).
    TODO: default cache file to start from scratch

    time to check /
    last check
    last_read
    """

    def __init__(self, sid_cache_file, do_cache_file=True, EOL='\n'):
        """
        sid_cache_file is a file containing Sid strings, one per line (separated by EOL).
        sid_cache_file should be a Path or path string.

        If do_cache_file is True (default) the file is converted to a list (loaded in RAM),
        else it is opened as a generator (reread at each usage).
        In case of large cache files, it is likely faster to set do_cache_file to False.

        TODO: better error handling, to rule out problems in the input data (input, conf or cache).
        TODO: better newline handling. Maybe automatic strip in LS.
        """
        self.sid_cache_file = str(sid_cache_file)
        if do_cache_file:
            self.cache_list = list(open(self.sid_cache_file, 'r'))
            self.ls = LS(searchlist=self.cache_list, do_strip=True)  # file is loaded in a list
        else:
            self.cache_list = None
            self.ls = None
        self.EOL = EOL
        debug('Init of SidCache with file {} (EOL= {})'.format(sid_cache_file, EOL))

    def __get_lists(self):
        """
        Accessor for self.cache_list and self.ls.
        Its goal is to update the objects if the underlying cache file was updated.
        It compares the file modification time to its read time.
        """

    def get(self, search_sid, as_sid=True):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file), do_strip=True)
        return ls.get(str(search_sid), as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file), do_strip=True)
        return ls.get_one(str(search_sid), as_sid=as_sid)

    def exists(self, search_sid):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file))
        return bool(first(ls.star_search([str(search_sid) + self.EOL], as_sid=False)))

    def create(self, new_sid=None, new_sids=[], fast=True, do_extrapolate=False, do_conform=False):
        """
        Adds the given new_sid and new_sids to the saved file cache.

        If fast is True, just appends to the file, without any checks.
        If fast is False, loops through the list, and appends only elements that are not there already

        If do_conform is True, data is inserted, then conformed, then written to the file (fast is ignored)

        Note on threadsafety.
        Write operations are kept atomic: either a simple append, or a complete replacement of the file.

        """
        if new_sid:
            new_sids.insert(0, new_sid)

        # simple approach: fast and not do_conform
        if fast and not do_conform:
            with open(self.sid_cache_file, 'a') as f:
                for sid in new_sids:
                    f.write(str(sid) + self.EOL)
            return

        # approaches with verification - we need the file as a list
        ls = self.cache_list  # WIP: load

        # simple approach with conform
        if do_conform:
            for sid in new_sids:
                ls.append(str(sid))


    def conform(self, do_uniquify=True, do_sort=True):
        """
        Conforms the current cache, using the given settings (do_uniquify, do_sort)
        """
        ls = self.cache_list  # or LS(searchlist=list(open(self.sid_cache_file, 'r')), do_strip=True)  # file is loaded in a list

    def __conform(self, cache_list):
        """
        Conforms the given list:
        Uniquify and sorting.
        """
        return sorted(list(set(cache_list)))

    def __replace(self, cache_list):
        """
        Replaces the current cache file with the given list.
        """
        import time
        temp_filename = self.sid_cache_file + str(time.time())
        with open(self.sid_cache_file, 'a') as f:
            for sid in cache_list:
                f.write(str(sid) + self.EOL)
        Path(temp_filename).replace(self.sid_cache_file)

    def delete(self):
        """

        """
        pass

    def init(self, source=None):
        pass


if __name__ == '__main__':

    """
    Idea: a "Cache Crawler"
    from a given Sid, crawls and fills the cache with neighbours, or related, or potentially nearly called Sids.
    
    It does so in an async process (if the cache is on disk, or in a thread (memcache).
    while the user is busy doing something else, or either time or CPU are iddle.
    It would be a non-blocking low priority process.
    """

    import sys
    """
    In the Data config, a Sidcache is associated to 
    - a file
    - a datasource to init the cache from
    
    then the cache maintains multiple levels: 
    - memory
    - the file 
    - the read only reference data source
    
    The cache is not used to write to the data source.
    The cache can be written to, to avoid a total reset.
    
    There are some delays: 
    - interval between the file date is checked
    - if updated (file date), the file is read again in memory
    - interval for needed file update
    
    When do we read from the reference data source ?
    """




    from spil.util.log import setLevel, DEBUG

    setLevel(DEBUG)

    sid_cache_file = 'V:/TESTPREMIERE/sids.test.txt'

    sd = SidCache(sid_cache_file)
    for i in sd.get('*/*/*'):  #
        print(i)

    sd2 = SidCache(sid_cache_file)
    print(sd2.get_one('CBM/A/CHR'))
    print(sd2.exists('TEdfsST'))
    print(sd2.exists('CBM/A'))

    sid = Sid('CBM')
    print(sid)
    # print(sid.get_last())

    """
    TODO: (in order of importance)
    
    - build from datasource, from scratch
    That makes the cache usable.
    Instead of editing it, we reread all X intervalls, or if 
    
    """
