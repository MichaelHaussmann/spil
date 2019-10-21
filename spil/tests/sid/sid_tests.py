
from pprint import pprint

from spil.libs.sid import Sid
from spil.libs.sid.sid import ShotSid, ProjectSid, AssetSid  # Needed for eval test

import inspect

test_params = {}


def get_member_names(obj):
    attributes = inspect.getmembers(obj)  # , lambda a: not (inspect.isroutine(a)))
    return [e[0] for e in [a for a in attributes if not (a[0].startswith('_'))]]


def get_members(obj, param=None):  # FIXME : proper attribute test
    result = {}
    for name in get_member_names(obj):
        attribute = getattr(obj, name, '--NOT SET--')
        if callable(attribute):
            #attribute()
            try:
                result[name] = attribute()
            except TypeError as te:
                if param:
                    try:
                        result[name] = attribute(param)
                    except Exception as e:
                        warn(e)
                        result[name] = 'ERROR'
                else:
                    result[name] = 'ERROR'
        else:
            result[name] = attribute
    return result


if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, warn

    print('')
    print('Tests start')
    print('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.sid_conf import test_sids as tests

    test_sids = []

    for test in tests:

        print('Testing : {}'.format(test))
        print('')
        sid = Sid(test)
        pprint(sid)
        assert (eval(repr(sid)) == sid)
        assert (test == str(sid))
        print('')
        pprint(sid.asdict())
        print('')
        pprint(get_members(sid))
        print('')
        print('*' * 30)
        print('')
        test_sids.append(sid)

    print('')
    print('*' * 30)
    print('')

    print('Sorted : ')
    pprint(sorted(test_sids, reverse=True))