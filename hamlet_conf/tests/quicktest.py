from spil import Sid
from spil import FindInPaths as Finder

if __name__ == '__main__':

    from spil_tests import stop
    from pprint import pprint
    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(INFO)

    for sid in Finder().find('hamlet/a/char/*'):
        print(f"Found: {sid}")

    # Test get_new('version')
    print("-" * 20)
    sid = Sid('hamlet/a/char/john')
    print(f"sid: {sid} - {repr(sid)}")

    print("-" * 20)
    # sid = Sid('hamlet/s/sq01/sh010/anim/*/w/ma')
    sid = Sid('hamlet/s/sq001/sh0010/anim')
    print(f"sid: {sid} - {repr(sid)}")

    print("-"*20)
    new_scene = sid.get_with(version='*', state='w', ext='ma')
    print(f"new scene: {new_scene}")
    print(new_scene.type)

    stop()