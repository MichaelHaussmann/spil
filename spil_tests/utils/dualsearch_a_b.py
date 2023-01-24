# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
"""
To launch searches on two finders. 
Allows comparing of finders.

Searches is a dict with searches as 
    key: read sid
    value: read description 

"""
from codetiming import Timer
from spil.util.log import DEBUG, ERROR, get_logger

log = get_logger("spil_tests")
log.setLevel(DEBUG)


def test_search_ab(searches, finderA, finderB, as_sid=False, replace=None):

    log.debug("Searching sids in A:{} and B:{}".format(finderA, finderB))

    global_timer = Timer(name="global", logger=log.debug)
    global_timer.start()

    for search_sid, comment in searches.items():

        log.info("*" * 10)
        log.info("{} --> {}".format(search_sid, comment))

        a_timer = Timer(name="a_timer", logger=log.info)
        a_timer.start()
        found_a = set(finderA.find(search_sid, as_sid=as_sid))
        log.info("A : {}".format(len(found_a)))
        a_timer.stop()

        b_timer = Timer(name="b_timer", logger=log.info)
        b_timer.start()
        found_b = set(finderB.find(search_sid, as_sid=as_sid))
        log.info("B : {}".format(len(found_b)))
        b_timer.stop()

        problems = found_b ^ found_a

        for i in problems:
            log.warning("Not equal in both searches: {}".format(i))

    log.debug("*" * 10)
    log.debug("Done all searches.")
    global_timer.stop()


if __name__ == "__main__":

    from spil import FindInList, FindInPaths, FindInAll
    from spil.util.log import setLevel, ERROR, DEBUG

    setLevel(ERROR)

    searches = {}
    searches["*"] = "projects"
    searches["hamlet/*"] = "types"
    searches["hamlet/a/*"] = "asset types"
    searches["hamlet/a/*/*"] = "assets"

    fpl = FindInPaths('local')
    fps = FindInPaths('server')
    # fl = FindInList(sids)
    ft = FindInAll()

    test_search_ab(searches, ft, fpl)
    # to compare speed, run the test twice and check second time.
    # test_search_ab(searches, fpl, ft)
