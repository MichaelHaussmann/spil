"""
Tests Getters by querying test sids.
(see also getter_search_tests)

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

from spil.util.log import DEBUG, get_logger

log = get_logger("spil_tests", color=False)

log = get_logger("spil_tests")

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    random.seed(26)
    random.shuffle(sids)

    getter_p = GetFromPaths()
    getter_a = GetFromAll()

    for _sid in sids[:50]:
        sid = Sid(_sid)
        print(sid)

        data1 = getter_a.get_one(sid)
        data2 = getter_p.get_data(sid)

        pprint(data1)
        pprint(data2)

        print(getter_a.get_attr(sid, "author"))
        print(getter_p.get_data(sid, attributes=["comment", "status"]))
        print("=" * 50)
