"""
This test runs tests on "data" Sid objects.
Data Sid objects contain attribute calls like
"sid.children()"
which are delegated to Finders and Getters (FindInAll and GetFromAll by default)

Uses the example sids.
"""
import random

# import spil  # config path bootstrap
from hamlet_scripts.example_sids import sids  # type: ignore
from spil.tests.utils.sid_data_tester import check_data_sids


def test_data_sids():

    random.seed(26)
    random.shuffle(sids)
    tests = sids[:20]
    check_data_sids(tests, reraise=True)


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO
    setLevel(INFO)
    test_data_sids()
