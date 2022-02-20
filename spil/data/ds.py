from spil import Sid
#from spil.conf import pre_search_update
from spil.util.log import debug, warn, info, error

from spil.data.data import get_data_source
from spil.sid.search.ss import SidSearch
from spil.sid.search.util import first
from spil.sid.search.tools import unfold_search


class Data(SidSearch):
    """
    Data abstraction Layer.

    On top of the built-in FS, and delegating data access to other custom Data sources.
    """

    def get(self, search_sid, as_sid=True):
        """
        Search dispatcher.

        :param search_sid:
        :param as_sid:
        :return:
        """
        # we start by transforming
        search_sids = unfold_search(search_sid)

        done = set()  #TEST

        for ssid in search_sids:

            source = get_data_source(ssid)

            if source:
                debug('Searching "{}" using "{}"'.format(ssid.full_string, source))
                generator = source.get(ssid, as_sid=as_sid, is_unfolded=True)

                for i in generator:
                    if i not in done:  # FIXME: check why data is so often repeated, this is expensice, optimize
                        done.add(i)
                        yield i

            else:
                warn('No data source found for "{}"'.format(ssid.full_string))

    def get_one(self, search_sid, as_sid=True):

        found = first(self.get(search_sid, as_sid=False))  # search is faster if as_sid is False
        if as_sid:
            return Sid(found)
        else:
            return found

    def exists(self, search_sid):  # TODO: evaluate best implementation
        source = get_data_source(search_sid)
        if source:
            return source.exists(search_sid)

    def create(self, sid):
        # FIXME: this is a stub.
        return
        destination = get_data_destination(sid)
        if destination:  # and hasattr(destination, 'create'):
            return destination.create(sid)


if __name__ == '__main__':

    from spil.util.log import setLevel, DEBUG, ERROR

    setLevel(ERROR)
