import spil_data_conf
from scripts.example_sids import sids
from spil_tests.utils.sid_path_test import test_path_sids

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    import random

    random.shuffle(sids)

    configs = list(spil_data_conf.path_configs)
    test_path_sids(sids, configs=configs)
