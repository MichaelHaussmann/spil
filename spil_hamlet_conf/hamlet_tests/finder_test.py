"""
This test runs and compares Finders.

Use test sids and the created test files.
"""
import random

from hamlet_scripts.example_sids import sids  # type: ignore

# from spil_plugins.sg.find_sg import FindInSG
from spil import FindInList, FindInPaths, FindInAll
from spil.tests.prep.build_searches import from_sid_build_searches
from spil.tests.utils.search_tester import check_searches_in_finder

from spil.util.log import get_logger
from spil.tests.utils.dualsearch_ab_tester import check_search_ab

log = get_logger("spil_tests", color=False)

def test_finders():

    random.seed(26)
    random.shuffle(sids)

    log.info("Starting Finder Tests")
    find_in_list = FindInList(sids)
    find_in_paths_local = FindInPaths("local")
    find_in_paths_server = FindInPaths("server")
    find_in_all = FindInAll()
    #     finder_in_sg = FindInSG()

    finders = [find_in_list, find_in_paths_local, find_in_paths_server, find_in_all]

    # sample Sids that will generate searches
    for sid in sids[:1]:

        log.info(f"Base Sid: {sid}")
        searches = from_sid_build_searches(sid)
        print("#" * 100)

        for search_sid, comment in searches.items():
            log.info(f"Running search: {search_sid}")
            search = {search_sid: comment}

            log.info("Comparing finders")
            check_search_ab(search, find_in_list, find_in_all, raise_problems=True)
            check_search_ab(search, find_in_paths_server, find_in_paths_local, raise_problems=True)

            print("-" * 50)
            for finder in finders:
                log.info(f"Running searches on {finder}")
                check_searches_in_finder(
                    search, finder, reraise=True  # , do_deep=(finder == find_in_list)
                )


if __name__ == "__main__":

    from spil.util.log import INFO
    log.setLevel(INFO)
    test_finders()
