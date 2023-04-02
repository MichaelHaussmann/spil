"""
This test runs basic, "core" tests on Sid objects.

Uses the example sids.
"""
import random

from hamlet_scripts.example_sids import sids  # type: ignore
from spil.tests.utils.sid_core_tester import check_typed_sids
from spil.util.log import setLevel, INFO

def test_typed_sids():

    random.seed(26)
    random.shuffle(sids)
    tests = sids[:100]
    check_typed_sids(tests)


if __name__ == "__main__":

    setLevel(INFO)
    test_typed_sids()
