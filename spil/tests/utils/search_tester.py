"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil import Sid, FindInPaths, SpilException
from spil.tests.utils.sid_full_tester import test_full_sid
from spil.util.log import get_logger
from spil.tests import Timer

log = get_logger("spil_tests")

"""
To launch searches on a custom Finder.

Searches is a dict with searches as 
    key: search sid
    value: search description 

"""

def check_searches_in_finder(searches, finder=None, as_sid=True, do_log=True, do_deep=False, do_doublon_check=True, do_match_check=False, replace=None, reraise=True):
    """
    Runs given searches on the given Finder.

    Optionally operates a replace in the read, using given replace tuple.
    """

    global_timer = Timer(name="global", logger=log.info)
    global_timer.start()

    finder = finder or FindInPaths()
    for search_sid, comment in searches.items():

        log.info("*" * 10)
        log.info("{} --> {} (finder: {})".format(search_sid, comment, finder))
        double_check = set()

        try:
            f_timer = Timer(name="search_sid", logger=log.info)
            f_timer.start()
            count = 0
            for i in finder.find(search_sid, as_sid=as_sid):
                if do_log:
                    log.info(i)
                if do_match_check:
                    match = Sid(i).match(search_sid)
                    if not match:
                        log.warning('No match "{}" <-> "{}". This is not normal'.format(i, search_sid))
                count += 1
                if do_doublon_check:
                    if i in double_check:
                        log.warning("--------------------------------------> Doublon {}".format(i))
                    double_check.add(i)
                if do_deep:
                    log.debug("Sid test for {}".format(i))
                    test_full_sid(i, from_search=search_sid)

            log.info("Total: " + str(count))
            f_timer.stop()

        except SpilException as e:
            log.error("SpilException : {} --> {}".format(e, search_sid))
            if reraise:
                raise e

    global_timer.stop()


if __name__ == "__main__":

    from spil.util.log import setLevel, ERROR

    setLevel(ERROR)

    searches = {}
    searches["hamlet/s/*/*"] = ""

    check_searches_in_finder(searches)
