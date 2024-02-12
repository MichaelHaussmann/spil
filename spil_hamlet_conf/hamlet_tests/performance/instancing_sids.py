from codetiming import Timer
from spil import Sid
from spil_hamlet_conf.hamlet_scripts.example_sids import sids

def instance_sids(sids, msg=""):
    t = Timer()
    t.start()
    for s in sids:
        sid = Sid(s)
    t.stop()
    bw = t.last / float(len(sids)) * 1000
    print(f"{msg}: {bw} ms/sid")

if __name__ == "__main__":

    # Important note:
    # The first calls have a cold a cold memory cache, and are slower.

    print("start")
    sids = list(sids[:2000])  # amount of Sids per cycle

    # import cProfile  # profiling
    # cProfile.run('instance_sids(sids, "prof")', sort=1)

    for i in range(5):  # amount of cycles
        instance_sids(sids, i)
    # instance_sids(sids, "Cached")
    print("done")