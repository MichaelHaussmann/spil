from spil_tests.utils.test_utils import test_sids


if __name__ == "__main__":

    from spil.util.log import setLevel, INFO, DEBUG, ERROR

    setLevel(ERROR)

    print()
    print("Sid test starts")

    sids = [
        "tp",
        "tp/*",
        "tp/a",
        "*",
        "*/*",
        "*/s/*",
    ]

    test_sids(sids, reraise=True)
