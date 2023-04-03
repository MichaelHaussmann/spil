# type: ignore
"""
https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes

"""

import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs  # noqa


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("pytest session start, setting up files if needed.")
    mfs.run()