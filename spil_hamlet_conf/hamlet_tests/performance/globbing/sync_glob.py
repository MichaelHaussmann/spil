from codetiming import Timer
from pathlib import Path

def main():
    root = Path("/home/mh/PycharmProjects/spil2/spil_hamlet_conf/data/testing/SPIL_PROJECTS")
    counter = 1
    for f in root.glob("**"):
        # print(f)
        pass
        counter += 1
    print(counter)


t = Timer()
t.start()
main()
t.stop()