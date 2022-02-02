import time
import os
from time import sleep

from spil import Sid
from spil.util.pool import Pooled

from spil.util.log import debug
from spil.sid.search.ls import LS, extrapolate
from spil.sid.search.ss import SidSearch
from spil.sid.search.util import first

from spil_tests.utils import Timer  #FIXME: proper timer

import six
if six.PY2: from pathlib2 import Path   # noqa
else: from pathlib import Path          # noqa

from spil import logging
log = logging.get_logger(name="sid_cache")
log.setLevel(logging.ERROR)

EOL = '\n'


def now():
    """ Returns the 'now' timestamp as an int """
    return int(time.time())


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

    def __init__(self, sid_cache_file, data_search, data_source=None):
        """
        sid_cache_file is a file containing Sid strings, one per line (separated by EOL).
        sid_cache_file should be a Path or path string.

        If do_cache_file is True (default) the file is converted to a list (loaded in RAM),
        else it is opened as a generator (reread at each usage).
        In case of large cache files, it is likely faster to set do_cache_file to False.

        TODO: better error handling, to rule out problems in the input data (input, conf or cache).
        TODO: better newline handling. Maybe automatic strip in LS.
        """
        # defining entry
        self.cache_path = Path(str(sid_cache_file))
        self.cache_list = []
        self.last_check_time = 0
        self.last_read_time = 0

        # configuration: data sourcce and searchkey
        if not data_source:
            from spil import FS, Data
            self.data_source = Data()  # test - datasource is any implementing SidSearch ?
        else:
            self.data_source = data_source
        self.data_search = data_search  # '*/A/*/*/*'

        # starting
        self._check()
        log.debug('Init of SidCache with file {}'.format(self.cache_path))

    def get(self, search_sid, as_sid=True):
        self._check()
        return self.ls.get(str(search_sid), as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        self._check()
        return self.ls.get_one(str(search_sid), as_sid=as_sid)

    def exists(self, search_sid):
        self._check()
        return bool(first(self.ls.star_search([str(search_sid)], as_sid=False)))   # [str(search_sid) + self.EOL] ?

    def create(self, sid, do_extrapolate=False):
        """
        Appends the given sid to cache_list and cache_file.

        Note on threadsafety.
        Write operations are kept atomic: either a simple append, or a complete replacement of the file.

        """
        self._read()
        if sid not in self.cache_list:
            with open(self.cache_path, 'a') as f:
                f.write(str(sid) + EOL)
            self.cache_list.append(str(sid))

    def init(self):
        """
        Inits the cache from the data source, from scratch.
        """

        ls_timer = Timer(name="fill")
        ls_timer.start()

        temp_path = self.cache_path.with_stem('temp_{}'.format(time.time()))
        temp_list = []
        with open(temp_path, 'a') as f:
            for sid in extrapolate(self.data_source.get(self.data_search, as_sid=False)):
                f.write(sid + EOL)
                temp_list.append(sid)
        Path(temp_path).replace(self.cache_path)

        self.cache_list = temp_list
        self.ls = LS(searchlist=self.cache_list)

        self.last_read_time = now()
        self.last_check_time = now()
        ls_timer.stop()

    def _read(self):
        if not self.cache_path.exists():
            log.debug('file does not exist, init')
            self.init()  # cold start
            return
        log.debug('reading file into memory')
        self.cache_list = [l.rstrip() for l in open(self.cache_path, 'r')]
        self.ls = LS(searchlist=self.cache_list)  # we hope the reference will stay after update of self.cache_list TODO: test
        self.last_read_time = now()

    def _check(self):
        log.debug('check')
        if now() > self.last_check_time + 30:
            log.debug('file date check is due')
            self.last_check_time = now()
            try:
                file_time = os.path.getmtime(str(self.cache_path))
            except FileNotFoundError:
                self.init()
                return
            if file_time > self.last_read_time:
                self._read()


if __name__ == '__main__':

    """
    Idea: a "Cache Crawler"
    from a given Sid, crawls and fills the cache with neighbours, or related, or potentially nearly called Sids.
    
    It does so in an async process (if the cache is on disk, or in a thread (memcache).
    while the user is busy doing something else, or either time or CPU are iddle.
    It would be a non-blocking low priority process.
    """

    from spil_tests.utils import stop
    import os

    log.setLevel(logging.DEBUG)

    sid_cache_file = 'V:/TESTPREMIERE/cache_test.txt'
    sd = SidCache(sid_cache_file, 'CBM/A/**')
    # '*/A/*/*/*'

    for i in range(100):
        sleep(3)
        print(sd.get_one('CBM/A/CHR'))

    stop()

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

    from spil.util.log import setLevel, DEBUG, INFO, ERROR

    setLevel(ERROR)

    sid_cache_file = 'V:/TESTPREMIERE/cache_test.txt'

    sd = SidCache(sid_cache_file)
    # sd.fill()

    print(sd.get_one('CBM/A/CHR'))

    ls_timer = Timer(name="fill")
    ls_timer.start()
    for i in sd.get('CBM/A/CHR/*'):  #
        print(i)
    ls_timer.stop()

    import time
    for i in range(1000):
        print(time.time())

    stop()

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
    
    - data query, check-time, and read-time
    
    when data is asked from the cache, it looks at the last file check time (check-time).
    if check time is older than xxx, we re-check: checks if the file was changed since last read (using file date).
    check-time gets updated to now.
    
    if the update time is newer than last read time (read-time), we re-read.
    read-time gets updated to now.
    
    - Ensure the SidCache instances are pooled 
    """
