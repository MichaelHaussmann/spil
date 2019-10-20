

from spil.libs.fs.core.fs_resolver import path_to_dict, dict_to_path
from spil.libs.util.exception import SpilException
from spil.libs.util.log import debug, warn, info


if __name__ == '__main__':

    import sys
    from pprint import pprint
    from spil.libs.sid import Sid

    def by_path(tests):

        for test in tests:

            info('Testing : {}'.format(test))
            info('')

            _type, _dict = path_to_dict(test)

            if _type:
                info('Match!')
            else:
                info('No match.')
                continue
            info('Resolved basetype : {}'.format(_type))
            info('Resolved dict : {}'.format(_dict))
            info('')
            if _type in ['shot_version']:  # FIXME : explicit conf
                info('This type cannot be resolved to a  path : {}. Skipped'.format(_type))
                continue

            retour = dict_to_path(_dict)
            info('Retour path : {}'.format(retour))
            assert (test == retour)

            info('')
            info('*' * 30)
            info('')

    def by_sids(tests):

        for test in tests:

            info('Testing : {}'.format(test))
            info('')

            test = Sid(test)

            _dict = test.asdict()
            _type = test.sidtype()
            info('Initial sid dict : {}'.format(_dict))
            info('Initial sid basetype : {}'.format(_type))

            path = None
            try:
                path = dict_to_path(_dict)
                info('Resolved to path : {}'.format(path))
            except SpilException as e:
                info('Unable to resolve path because : {}'.format(e))

                test = test.parent(set_default=True)  # we try to level one up
                if test:
                    info('Sid up one level (parent)...')
                    warn('Sid is now : {}'.format(test))
                    _dict = test.asdict()
                    _type = test.sidtype()
                    info('Sid dict is now : {}'.format(_dict))
                    path = dict_to_path(test.asdict())  # do not catch error if this doesnt work
                    info('Resolved to path : {}'.format(path))

            _type, retour = path_to_dict(path)

            if _type:
                info('Retour resolved')
            else:
                info('No match.')
                continue

            info('Resolved retour dict : {}'.format(retour))
            info('')
            # assert (_dict == retour)  # dicts do not need to be identical.

            retour = Sid(data=retour)
            info('Retour sid : {}'.format(retour))
            info('')
            assert (test == retour)

            info('')
            info('*' * 30)
            info('')

    info('')
    info('*' * 30)
    info('')

    from spil.libs.util.log import setLevel, DEBUG, INFO, info, warn

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    info('')
    info('Tests start')
    info('')

    # by paths
    from spil.conf.fs_conf import test_paths as tests
    by_path(tests)

    # by sids
    from spil.conf.sid_conf import test_sids as tests
    by_sids(tests)
