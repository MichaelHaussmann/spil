import time
import os
from multiprocessing import Process

from spil.util.caching import lru_kw_cache as cache

from spil.sid.search.ls import extrapolate
from spil.sid.search.ss import SidSearch
from spil.sid.search.util import first

import six

if six.PY2:
    from pathlib2 import Path  # noqa
else:
    from pathlib import Path  # noqa

from spil import logging, Data, LS, SpilException

log = logging.get_logger(name="sid_cache")
log.setLevel(logging.ERROR)

EOL = "\n"
lock_outdate = 60 * 5  # 5 minutes
max_warmup_wait = 60  # 1 minute


def now():
    """Returns the 'now' timestamp as an int"""
    return int(time.time())


# @lru_cache
@cache
def get_sidcache(sid_cache_file, data_search, data_source=None):
    """
    Factory to build pooled SidCache objects.

    "Pooled" means:
        Each sid_cache_file is handled by its own, single, SidCache instance.
        A SidCache object handles only one sid_cache_file.
        For example:
            a = SidCache(sid_cache_file='/shots.txt')
            b = SidCache(sid_cache_file='/shots.txt')
            c = SidCache(sid_cache_file='/assets.txt')
            a and b will be the same object instance, and access the same data.
            c will be another object.

    Note that the file can be accessed concurrently from different python instances, from different machines.
    SidCache still needs to ensure threadsafety.

    #TODO: replace lru cache with a custom cache, with only filename as key.
    """
    return SidCache(sid_cache_file, data_search, data_source=data_source)


class SidCache(SidSearch):
    """
    Simple Sid cache implementation.
    It holds only Sids, not data related to Sids.
    It implements Data with methods: get, get_one, exists, create.

    There are 3 cached levels:
    - the LS ListSearch object, the cache in memory
    = a cache file on disk, the cache on disk for concurrent reads and updates
    = the original data source, that is to be cached.

    The cache can have 3 states:
    - hot: the Sids are cached in memory, in form of a LS (List Source) object.
      The clients can be served from the cache.
    - warm: the Sids are in a cache file on disk, but not yet loaded in memory, or outdated in memory.
      The cache needs to be loaded in memory, then it serves the client.
    - cold: no cache file exists, the file needs to be created and filled using the original data source.
      The SidCache will fill the file in the background (another process), and serve the client with the original data source.

    The workflow:
    - The cache initially reads the original data source into a file (warming up)
      During warmup, the cache serves the client via the original data source
    - When the file exists, it is read into memory (heating up)
      Now the cache is hot and serves clients
    - regularly, the cache checks if the file was updated since last read.
      If so, it re-reads it in memory.
    - The file is updated from concurrently existing SidCache instances.
      Thanks to the updates, the cache can be warm for a potentially indefinite time

    This cache implementation is very simple, and tailored to its working environment.
    It works well as long as:
    - Writes to the cache are rather rare, and reads are frequent
    - The cache is explicitly updated whenever the original data source is updated
      (so the cache can stay warm, because warming is slow)
    - The files are kept small, meaning the data is stored in multiple caches
      (under 5K items per cache)
    - Note: simultaneous writing of the same Sid may produce its duplication in the cache.

    The cache usage is simple and straightforward.
    get a new object via the factory function get_sidcache, by passing
    - a file path, for the cache file
    - a search sid and a data source, that will be the original data source.

    Typically, setting up the different caches for one or more projects is handled in the data_conf.
    The defined caches are then mapped to serve as data sources.

    Example:
        Setting up a cache on file '/temp/hamlet_shots.txt'
        For 'hamlet/s/*/*/*' (sequences, shots and tasks for hamlet project)
        Originally loaded from FS (File Search).
    ```
    >>> sidcache = get_sidcache(sid_cache_file='/temp/hamlet_shots.txt', data_search='hamlet/s/*/*', data_source=FS())
    >>> sidcache.get('hamlet/s/*')
    ```
    TODO: optional multiple data sources
    TODO: ttl for warmup
    TODO: file conform (dedoublon, sort) in background process
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
        self.ls = None
        self.last_check_time = 0
        self.last_read_time = 0
        self.ttl = 30  # Minimal interval in seconds, before we check if the cache file modification time has been changed.

        # configuration: data source and searchkey
        if not data_source:
            from spil import FS, Data

            # Use list of data sources in Data ? What to do if this cache is included in Data ?
            self.data_source = FS()  # , Data()  # test - datasource is any implementing SidSearch ?
        else:
            self.data_source = data_source
        self.data_search = data_search  # '*/A/*/*/*'

        # starting
        self._source()
        log.info("Init of SidCache with file {}".format(self.cache_path))

    def get(self, search_sid, as_sid=True):
        return self._source().get(str(search_sid), as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        return self._source().get_one(str(search_sid), as_sid=as_sid)

    def exists(self, search_sid):
        return bool(first(self._source().get_one([str(search_sid)], as_sid=False)))

    def create(self, sid, do_extrapolate=False):
        """
        Appends the given sid to cache_list and cache_file.

        Note on threadsafety.
        Write operations are kept atomic: either a simple append, or a complete replacement of the file.

        """
        if not self.cache_path.exists():
            log.debug("File does not exist, cache is cold, needs blocking warm up.")
            self._warm_up(blocking=True)
        self._heat_up()
        # this is not thread safe. It could happen that the data gets inserted twice. But it cannot be lost.
        if sid not in self.cache_list:
            with open(self.cache_path, "a") as f:
                f.write(str(sid) + EOL)
            self.cache_list.append(str(sid))
            self.ls = LS(searchlist=self.cache_list)

    def _source_to_file(self):
        """
        Reads the original data source into the cache file.

        """
        log.info("Start _source_to_file on {}".format(self.cache_path))
        lock = self.cache_path.with_suffix(".lock")
        temp_path = self.cache_path.with_name(
            "temp_{}".format(time.time()) + self.cache_path.suffix
        )
        generated = set()
        with open(temp_path, "a") as f:
            for search in extrapolate([self.data_search]):
                if not search.endswith("*"):
                    continue
                print("searching " + search)
                for sid in extrapolate(self.data_source.get(search, as_sid=False)):
                    if sid in generated:
                        continue
                    generated.add(sid)
                    f.write(sid + EOL)
        Path(temp_path).replace(self.cache_path)
        lock.unlink()
        log.info("Done _source_to_file on {}".format(self.cache_path))

    @staticmethod
    def __wait_for_warmup(lock):
        """
        Waits as long as the given lock file exists.
        In case of time out, raises an exception.

        This is used by a SidCache that needs to wait for the warmup to complete, typically to insert data.
        """
        for i in range(max_warmup_wait):
            if lock.exists():
                time.sleep(1)
            else:
                return
        lock.unlink()
        raise SpilException(
            "Exhausted timeout ({} seconds) while waiting for cache warmup lock, file {}".format(
                max_warmup_wait, lock
            )
        )

    def _warm_up(self, blocking=False):
        """
        Inits the cache from the data source, from scratch.

        The warmup (cache reading function _source_to_file) is launched in a new process, protected by a lock file.

        If blocking is True, we wait for completion before returning.
        If blocking is False, we return the original data source, to serve the cache clients during warmup.
        """
        # check if no warmup already in process
        lock = self.cache_path.with_suffix(".lock")
        if lock.exists():
            if now() > os.path.getmtime(str(lock)) + lock_outdate:
                log.debug("Warmup lock is outdated, will be removed for warmup relaunch.")
                lock.unlink()
            else:
                log.debug("Warmup process already ongoing")
                if blocking:
                    log.debug("Waiting for warmup to finish before returning")
                    self.__wait_for_warmup(lock)
                else:
                    log.debug("Returning original data source")
                    return self.data_source

        lock.touch()
        p = Process(target=self._source_to_file)
        p.start()
        if blocking:
            # we do not p.join because we want to raise Exception if wait was too long
            self.__wait_for_warmup(lock)
            log.info("Warm_up finished for {}".format(self))
        else:
            log.info("Warm_up launched for {}".format(self))

    def _heat_up(self):
        """
        The cache file is loaded into memory.
        This process is blocking.
        """

        if not self.cache_path.exists():
            log.debug("File does not exist, cache is cold, needs warm up.")
            return self._warm_up()

        log.debug("File exists, reading file into memory (heating up)")
        if six.PY2:  # TODO: check if file gets closed in PY2.
            self.cache_list = [line.rstrip() for line in open(str(self.cache_path), "r")]
        else:
            self.cache_list = [line.rstrip() for line in open(self.cache_path, "r")]
        self.ls = LS(searchlist=self.cache_list)
        self.last_read_time = now()
        return self.ls

    def _source(self):
        """
        Checks for the Caches temperature, and returns the adequate data source.
        Either the LS object, if the cache is hot, or the original data source, if it is cold.

        Depending on the state of the cache, it launches heat-up prior to serving, or warm-up in the background.
        """
        log.debug("_source")
        if now() > self.last_check_time + self.ttl:
            log.debug("File date check is due")
            try:
                file_time = os.path.getmtime(str(self.cache_path))
                self.last_check_time = now()
            except FileNotFoundError:
                return self._warm_up()
            if file_time > self.last_read_time:
                return self._heat_up()

        return self.ls or self._heat_up()

    def __str__(self):
        return '<SidCache: "{}"@{} ({})>'.format(
            self.data_search, self.cache_path.name, self.data_source
        )

    def __repr__(self):
        return str(self)


if __name__ == "__main__":

    from spil_tests import stop
    import os

    log.setLevel(logging.DEBUG)

    sc = get_sidcache("V:/TESTPREMIERE/sdc.sids.txt", "FTOT/*/*")

    sc2 = get_sidcache("V:/TESTPREMIERE/ffm.sids.txt", "FFM/A,S,R/*/*/*")

    sc3 = get_sidcache("V:/TESTPREMIERE/sdc.sids.txt", "FTOT/*/*")

    assert sc == sc3

    print(get_sidcache.cache_info())
    for i in sc.get("FTOT/S/*"):
        print(i)

    for i in sc2.get("FFM/S/SQ0001/*"):
        print(i)

    # sc2.create('FFM/S/SQ0001/SH0007')

    for i in sc2.get("FFM/S/SQ0001/SH0007"):
        print(i)

    stop()
    # get_sidcache.cache_clear()

    print(list(Data().get("CBM/*")))

    print(list(Data().get("CBM/*")))

    print(list(Data().get("ARM/*")))

    # print(list(Data().get('FFM/A,S/*/*/*')))
    for i in Data().get("FFM/A,S/*/*/*"):
        print(i)

    sc4 = get_sidcache("V:/TESTPREMIERE/sdc.sids.txt", "CBM/*")

    get_sidcache.cache_info()
