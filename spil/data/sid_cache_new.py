import time
import os

from spil.util.caching import lru_kw_cache as cache

from spil.sid.search.ls import extrapolate
from spil.sid.search.ss import SidSearch
from spil.sid.search.util import first

import six
if six.PY2: from pathlib2 import Path   # noqa
else: from pathlib import Path          # noqa

from spil import logging, Data, LS

log = logging.get_logger(name="sid_cache")
log.setLevel(logging.ERROR)

EOL = '\n'


def now():
    """ Returns the 'now' timestamp as an int """
    return int(time.time())


# @lru_cache
@cache
def get_sidcache(sid_cache_file, data_search, data_source=None):
    """
    Factory to build pooled SidCache objects.
    """
    return SidCache(sid_cache_file, data_search, data_source=data_source)


class SidCache(SidSearch):
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
        log.info('Init of SidCache with file {}'.format(self.cache_path))

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
        # temp_path = self.cache_path.with_stem('temp_{}'.format(time.time()))  # with_stem is PY3.9
        temp_path = self.cache_path.with_name('temp_{}'.format(time.time()) + self.cache_path.suffix)
        temp_list = []
        generated = set()
        with open(temp_path, 'a') as f:
            for search in extrapolate([self.data_search]):
                if not search.endswith('*'):
                    continue
                print('searching ' + search)
                for sid in extrapolate(self.data_source.get(search, as_sid=False)):
                    if sid in generated:
                        continue
                    generated.add(sid)
                    f.write(sid + EOL)
                    temp_list.append(sid)
        Path(temp_path).replace(self.cache_path)

        self.cache_list = temp_list
        self.ls = LS(searchlist=self.cache_list)

        self.last_read_time = now()
        self.last_check_time = now()
        log.info('Init done for {}'.format(self))

    def _read(self):
        if not self.cache_path.exists():
            log.debug('file does not exist, init')
            self.init()  # cold start
            return
        log.debug('reading file into memory')
        if six.PY2:
            self.cache_list = [l.rstrip() for l in open(str(self.cache_path), 'r')]  # TODO: check if file gets closed in PY2.
        else:
            self.cache_list = [l.rstrip() for l in open(self.cache_path, 'r')]
        self.ls = LS(searchlist=self.cache_list)  # we hope the reference will stay after update of self.cache_list TODO: test
        self.last_read_time = now()

    def _check(self):
        log.debug('check')
        if now() > self.last_check_time + 30:
            log.debug('file date check is due')
            try:
                file_time = os.path.getmtime(str(self.cache_path))
                self.last_check_time = now()
            except FileNotFoundError:
                self.init()
                return
            if file_time > self.last_read_time:
                self._read()


if __name__ == '__main__':

    from spil_tests.utils import stop
    import os

    for i in extrapolate(['CBM/A/*/*/*']):
        print(i)
    stop()

    log.setLevel(logging.DEBUG)

    sc = get_sidcache('V:/TESTPREMIERE/sdc.sids.txt', 'CBM/*')

    sc2 = get_sidcache('V:/TESTPREMIERE/bla.sids.txt', 'CBM/*')

    sc3 = get_sidcache('V:/TESTPREMIERE/sdc.sids.txt', 'CBM/*')

    assert sc == sc3

    get_sidcache.cache_info()
    # get_sidcache.cache_clear()

    print(list(Data().get('CBM/*')))

    print(list(Data().get('CBM/*')))

    print(list(Data().get('ARM/*')))

    # print(list(Data().get('FFM/A,S/*/*/*')))
    for i in Data().get('FFM/A,S/*/*/*'):
        print(i)

    sc4 = get_sidcache('V:/TESTPREMIERE/sdc.sids.txt', 'CBM/*')

    get_sidcache.cache_info()
