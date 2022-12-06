from spil.sid.sid import Sid

if __name__ == '__main__':
    from spil_tests import stop
    from pprint import pprint
    from spil.util.log import debug, setLevel, INFO, DEBUG, info
    setLevel(INFO)

    # Test get_new('version')
    sid = 'hamlet/a/char/john'
    sid = Sid(sid)
    print(f"sid: {sid} - {repr(sid)}")


    print("-" * 20)
    sid = 'hamlet/s/sq001/sh0010/anim'
    # sid = 'hamlet/s/sq01/sh010/anim/*/w/ma'
    sid = Sid(sid)
    print(f"sid: {sid} - {repr(sid)}")


    print("-"*20)
    new_scene = sid.get_with(version='*', state='w', ext='ma')
    print(f"new scene: {new_scene}")
    print(new_scene.type)
    stop()