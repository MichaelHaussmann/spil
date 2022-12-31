import spil  # config path bootstrap
from scripts.example_sids import sids  # type: ignore
# from spil_plugins.sg.find_sg import FindInSG
from spil_tests.prep.build_searches import from_sid_build_searches
from spil_tests.utils.customsearch import test_searches_in_finder

from spil.util.log import DEBUG, get_logger

log = get_logger("spil_tests", color=False)


if __name__ == "__main__":

    from spil import FindInList, FindInPaths, FindInFinders

    from spil.util.log import setLevel, INFO

    log.setLevel(INFO)

    import random

    random.shuffle(sids)

    log.info("Starting Finder Tests")
    # finder = FindInList(sids)
    # finder = FindInPaths('local')
    # finder = FindInPaths('server')
    finder = FindInFinders()
#     finder = FindInSG()

    for sid in sids[0:1]:

        log.info(f'Base Sid: {sid}')
        searches = from_sid_build_searches(sid)

        log.info(f'Running searches... ')

        test_searches_in_finder(searches, finder, reraise=False)
