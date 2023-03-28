"""
This test runs tests on "path" Sid objects.
Path Sid objects implement path mapping.

Uses the example sids.
"""
import spil  # config path bootstrap
import spil_data_conf  # type: ignore
from scripts.example_sids import sids  # type: ignore
from spil_tests.utils.sid_path_test import test_path_sids

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    import random

    random.shuffle(sids)

    configs = list(spil_data_conf.path_configs)
    test_path_sids(sids, configs=configs)
