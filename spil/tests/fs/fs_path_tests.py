

from spil.libs.sid import Sid

if __name__ == '__main__':

    """
    This tests File -> Sid

    This tests gets the test_paths, generates sids and back to path again.

    """

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('')
    info('Tests start')
    info('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.fs_conf import test_paths as tests

    test_paths = []

    for test in tests:
        info('Testing : {}'.format(test))
        info('')

        sid = Sid(path=test)

        if not sid:
            info('Not matching, skipping : {}'.format(test))
            continue

        info('Resolved {}'.format(sid))

        retour = sid.path
        info('Retour path : {}'.format(retour))
        assert (test == retour)

        info('')
        info('*' * 30)
        info('')
        test_paths.append(test)

    info('')
    info('*' * 30)
    info('')

