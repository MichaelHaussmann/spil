"""
Tests Getters by querying "search sids" generated from test sids.
(see also getter_sid_tests)

Tests GetFromPaths, which reads json data written by WriteToPaths.

Tests GetFromAll, which delegates to other getters,
depending on the Sids type (as configured in spil_data_conf)

This is work in progress.
"""
from pprint import pprint
import random

import spil  # default config path bootstrap
from scripts.example_sids import sids  # type: ignore
from spil import Sid, GetFromPaths, GetFromAll
from spil_plugins.sg.find_sg import FindInSG
from spil_tests.prep.build_searches import from_sid_build_searches

from spil.util.log import DEBUG, get_logger

log = get_logger("spil_tests", color=False)

log = get_logger("spil_tests")

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO, ERROR

    setLevel(ERROR)

    random.seed(26)
    random.shuffle(sids)

    getter = GetFromPaths()
    # getter = GetFromAll()

    for _sid in sids[:3]:
        searches = from_sid_build_searches(_sid)
        for search, comment in searches.items():
            print("=" * 50)
            print(f"Search: {search} / {comment}")

            for data in getter.get(search):
                # for data in FindInSG().find(search):
                pprint(data)
                # data1 = getter.get_one(sid)
                # data2 = getter.get_data(sid)
                #
                # pprint(data1)
                # pprint(data2)

                # print(getter.get_attr(sid, "author"))
