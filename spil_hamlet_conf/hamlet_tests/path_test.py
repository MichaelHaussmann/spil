"""
This test runs tests on "path" Sid objects.
Path Sid objects implement path mapping.

Uses the example sids.
"""
import random

import spil_data_conf  # type: ignore
from hamlet_scripts.example_sids import sids  # type: ignore
from spil.tests.utils.sid_path_tester import check_path_sids


def test_path_sids():

    random.seed(26)
    random.shuffle(sids)
    tests = sids[:20]
    check_path_sids(tests, reraise=True)


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO
    setLevel(INFO)
    test_path_sids()
