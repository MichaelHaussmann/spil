# type: ignore
import spil  # default config path bootstrap
import spil_data_conf
from scripts.example_sids import sids
from spil_tests.prep.make_mock_fs import generate_mock_fs

if __name__ == '__main__':

    from spil.util.log import setLevel, INFO, DEBUG, info

    print('')
    print('Tests start')
    print('')

    # setLevel(WARN)
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    for config in list(spil_data_conf.path_configs):
        generate_mock_fs(sids, config=config)