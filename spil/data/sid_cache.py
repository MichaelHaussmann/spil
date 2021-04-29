# from abc import ABC

# from data_conf import sid_cache_file
from spil import LS
from spil.sid.search.ss import SidSearch

sid_cache_file = '/home/mh/Desktop/SID_DEMO/projects/sids.test.txt'


class SidCache(SidSearch):

    def __init__(self):

        self.ls = LS(searchlist=open(sid_cache_file, 'r'))

    def get(self, search_sid, as_sid=True):
        return self.ls.get(search_sid, as_sid=as_sid)

    def get_one(self, search_sid, as_sid=True):
        return self.ls.get_one(search_sid, as_sid=as_sid)


if __name__ == '__main__':

    sd = SidCache()
    for i in sd.get('*/*/*'):
        print(i)

    print(sd.get_one('*'))