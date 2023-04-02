# type: ignore
"""
https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes

"""
from contextlib import suppress

from spil import SpilException
import spil_data_conf
from hamlet_scripts.example_sids import sids
from spil.tests.prep.make_mock_fs import generate_mock_fs


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("pytest session start, setting up files if needed.")
    for config in list(spil_data_conf.path_configs):
        with suppress(SpilException):  # ignore exception if already exists
            generate_mock_fs(sids, config=config)
