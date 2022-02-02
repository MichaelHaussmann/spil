import unittest

from spil import Sid
from spil.data.sid_cache import SidCache


class MyTestCase(unittest.TestCase):

    def test_something(self):

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
        print(sid.get_last())  # this triggers a second pooled instance


if __name__ == '__main__':
    unittest.main()
