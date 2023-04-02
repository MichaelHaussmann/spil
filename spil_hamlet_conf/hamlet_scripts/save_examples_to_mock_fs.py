# type: ignore
"""
This script uses the test sids,
and generates empty but correctly named files,
according to the path configs.

"""
import spil_data_conf
from hamlet_scripts.example_sids import sids
from spil.tests.prep.make_mock_fs import generate_mock_fs

if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    print("")
    print("Tests start")
    print("")

    # setLevel(WARN)
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    for config in list(spil_data_conf.path_configs):
        generate_mock_fs(sids, config=config)
