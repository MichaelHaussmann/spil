"""
Little script running simple ad-hoc discovery tests.
"""
from spil import Sid
from spil import FindInPaths as Finder

if __name__ == "__main__":

    from spil.tests import stop
    from pprint import pprint
    from spil.util.log import setLevel, INFO

    setLevel(INFO)

    r = Sid("hamlet/s/sq010/sh0030/fx/v001/p/sword/vdb").type
    pprint(r)
    # print(Sid(path=path))
    # print(Sid("hamlet/s/sq010/sh0030/fx/v001/p/sword/vdb").path())
    # stop()

    # method chaining.
    s = (
        Sid()
        .get_with(project="hamlet", type="s")
        .get_with(query="sequence=sq010&shot=sh0010&task=anim")
        .get_as("project")
    )
    pprint(s)

    s = Sid(query="project=hamlet&type=s&sequence=sq010&shot=sh0010&task=anim")
    pprint(s)

    s = Sid("shot__sequence:hamlet/s/sq010")
    print(s.fields)

    for sid in Finder().find("hamlet/a/char/*"):
        print(f"Found: {sid}")

    # Test get_new('version')
    print("-" * 20)
    sid = Sid("hamlet/a/char/john")
    print(f"sid: {sid} - {repr(sid)}")

    print("-" * 20)
    # sid = Sid('hamlet/s/sq01/sh010/anim/*/w/ma')
    sid = Sid("hamlet/s/sq001/sh0010/anim")
    print(f"sid: {sid} - {repr(sid)}")

    print("-" * 20)
    new_scene = sid.get_with(version="*", state="w", ext="ma")
    print(f"new scene: {new_scene}")
    print(new_scene.type)

    stop()
