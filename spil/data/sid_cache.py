from spil import Sid
from spil.util.singleton import Singleton

from spil.util.log import debug
from spil.sid.search.util import first
from spil.sid.search.ls import LS
from spil.sid.search.ss import SidSearch


class SidCache(SidSearch, Singleton):
    """
    Simple Sid cache implementation, using LS ListSearch with a file.

    TODO: cache create/update.
    TODO: default cache file to start from scratch
    """

    def __init__(self, sid_cache_file, do_cache_file=True, EOL='\n'):
        """
        sid_cache_file is a file containing Sid strings, one per line (separated by EOL).

        If do_cache_file is True (default) the file is converted to a list (loaded in RAM),
        else it is opened as a generator (reread at each usage).
        In case of large cache files, it is likely faster to set do_cache_file to False.

        TODO: better error handling, to rule out problems in the input data (input, conf or cache).
        TODO: better newline handling. Maybe automatic strip in LS.
        """
        self.sid_cache_file = sid_cache_file
        if do_cache_file:
            self.ls = LS(searchlist=list(open(self.sid_cache_file, 'r')), do_strip=True)  # file is loaded in a list
        else:
            self.ls = None
        self.EOL = EOL
        debug('Init of SidCache with file {} (EOL= {})'.format(sid_cache_file, EOL))

    def get(self, search_sid, as_sid=True):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file), do_strip=True)
        return ls.get(str(search_sid), as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file), do_strip=True)
        return ls.get_one(str(search_sid), as_sid=as_sid)

    def exists(self, search_sid):
        ls = self.ls or LS(searchlist=open(self.sid_cache_file))
        return bool(first(ls.star_search([str(search_sid) + self.EOL], as_sid=False)))


if __name__ == '__main__':

    sid_cache_file = 'V:/TESTPREMIERE/sids.test.txt'

    sd = SidCache(sid_cache_file)
    for i in sd.get('*/*/*'):  #
        print(i)

    print(sd.get_one('CBM/A/CHR'))
    print(sd.exists('TEdfsST'))
    print(sd.exists('CBM/A'))

    sid = Sid('CBM')
    print(sid)
    print(sid.get_last())
