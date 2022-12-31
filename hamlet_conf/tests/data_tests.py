import spil  # config path bootstrap
from scripts.example_sids import sids  # type: ignore
from spil_tests.utils.sid_data_tests import test_data_sids

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    import random

    random.shuffle(sids)
    test_data_sids(sids, reraise=True)
