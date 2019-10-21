import os
from pprint import pprint

import six

from spil.libs.sid import Sid
from spil.libs.util.utils import is_filename

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path


if __name__ == '__main__':

    import sys

    from spil.libs.util.log import setLevel, DEBUG, INFO

    print('')
    print('Tests start')
    print('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    print('*' * 60)

    test_paths = []

    # tests = [r'Z:\Projects\Vic_Movie\Prod']

    # if not input('Create if not existing ?'):
        # sys.exit()

    from spil.conf.sid_conf import test_sids as tests

    test_sids = []

    for test in tests:

        sid = Sid(test)
        print('Sid : {}'.format(sid))

        # We fill defaults, but only until current type
        leaftype = sid.endtype()
        sid.set_defaults()
        print('Sid with defaults: {}'.format(sid))
        if leaftype != 'file':
            sid = sid.get_as(leaftype)
            print('Sid cut back: {}'.format(sid))

        path = sid.path
        if path:
            test_paths.append(path)
            print('Appended : {}'.format(path))

    for path in test_paths:
        path = Path(path)
        print( path )
        if not path.exists():
            if is_filename(path):
                print( path, 'is a file')
                if not path.parent.exists():
                    os.makedirs(str(path.parent))
                path.touch()
            else:
                print( path, 'is a dir')
                os.makedirs(str(path))

    print('Created test paths : ')
    pprint(test_paths)