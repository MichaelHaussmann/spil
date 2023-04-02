# type: ignore
"""
This script reads the Sids that have been saved to the example sid file.
The Sids are loaded into the "sids" variable to be used in tests.

The script can also launch a "test_config_coverage".
This shows all the types covered by the test sids,
and which types are not.
"""
from hamlet_scripts.save_examples_to_file import sid_file

sids = []
with sid_file.open() as f:
    sids = f.read().splitlines()

if __name__ == "__main__":

    import sys
    from spil.tests import Timer

    from spil.util.log import DEBUG, get_logger

    log = get_logger("spil_tests")
    log.setLevel(DEBUG)

    from spil import Sid

    print("Start")
    # pprint(sids)

    print(len(sids))

    if False:  # set False to skip
        test_config_coverage(sids)

    y = input("print out detail ?")

    if y != "y":
        sys.exit()

    global_timer = Timer(name="global", logger=log.debug)
    global_timer.start()
    for i, s in enumerate(sids):
        sid = Sid(s)
        if not sid:
            print(f"---------------------------------> {sid}")
            sleep(1)
        if i % 20 == 0:
            print(
                f"{i} -- {repr(sid)}",
            )

    global_timer.stop()
    print("Done")

    print(len(sids))

    global_timer = Timer(name="global", logger=log.debug)
    global_timer.start()
    for i, s in enumerate(sids):
        sid = Sid(s)
        if not sid:
            print(f"---------------------------------> {sid}")
            sleep(1)
        if i % 20 == 0:
            print(
                f"{i} -- {repr(sid)}",
            )
    global_timer.stop()
