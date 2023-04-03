# type: ignore
# noqa
"""
This script uses the test sids,
and generates empty but correctly named files,
according to the path configs.

"""
from contextlib import suppress

import spil_data_conf
from spil import SpilException
from hamlet_scripts.example_sids import sids
from spil.tests.prep.make_mock_fs import generate_mock_fs

def run():

    print("Starting generate_mock_fs.run()")

    for config in list(spil_data_conf.path_configs):
        with suppress(SpilException):  # ignore exception if already exists
            generate_mock_fs(sids, config=config)

    print("Done generate_mock_fs.run()")


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO

    print("")
    print("Tests start")
    print("")

    # setLevel(WARN)
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    run()
