
from spil.libs.sid import Sid

if __name__ == '__main__':

    """
    This tests Sid -> File

    This tests gets the test_sids, generates paths and back to sids again.
    
    """

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('')
    info('Tests start')
    info('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.sid_conf import test_sids as tests

    for test in tests:
        info('Testing : {}'.format(test))
        info('')

        sid = Sid(test)

        if not sid:
            info('Sid not correct, skipping : {}'.format(test))
            continue

        if sid.sidtype() in ['shot_version', 'asset_version']:  # FIXME : explicit conf
            info('This type cannot be resolved to a  path : {}. Skipped'.format(sid.sidtype()))
            continue

        path = sid.path
        info('Resolved path {}'.format(path))
        retour = Sid(path=path)

        info('Retour sid : {}'.format(retour))
        assert (sid == retour)

        info('')
        info('*' * 30)
        info('')

    info('')
    info('*' * 30)
    info('')

