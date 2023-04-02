"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from spil.util.log import DEBUG, get_logger
from spil import Sid, SpilException
from pprint import pformat

log = get_logger("spil_tests", color=False)
log.setLevel(DEBUG)


def check_path_sid(s, configs=[], reraise=True, replace=None):
    """
    Test protocol including Path operations: Sid(path=...) and sid.path().

    """
    s = str(s)
    if replace:
        s = s.replace(*replace)

    log.info('Testing: "{}"'.format(s))
    sid = Sid(s)
    log.info('Instanced: "{}"'.format(sid.uri))

    try:
        if not sid.type:
            log.error('Sid "{}" not typed, skipping'.format(sid))
            return

        path = sid.path()
        if path:
            try:
                assert sid == Sid(path=sid.path())
                log.info("Passed : sid == Sid(path=sid.path()) ")
            except AssertionError:
                msg = "Sid path is ambiguous. {}\nsid: {}\nsid.path(): {}\nSid(path=sid.path()): {}\n".format(
                    "(Sid is a search, this may be normal)." if sid.is_search() else "",
                    sid,
                    sid.path(),
                    Sid(path=sid.path()),
                )
                log.warning(msg)
            try:
                assert sid.path() == Sid(path=sid.path()).path()
                log.info("Passed : sid.path() == Sid(path=sid.path()).path() ")
            except AssertionError:
                msg = "Sid path is ambiguous. {}\nsid: {}\nsid.path(): {}\nSid(path=sid.path()): {}\nSid(path=sid.path()).path(): {}".format(
                    "(Sid is a search, this may be normal)." if sid.is_search() else "",
                    sid,
                    sid.path(),
                    Sid(path=sid.path()),
                    Sid(path=sid.path()).path(),
                )
                log.warning(msg)
        else:
            log.error('Sid "{}" has no path.'.format(sid))

        params = {
            "path": sid.path(),
        }
        for config in configs:
            params[f"path({config})"] = sid.path(config)

        log.info("Params: \n" + pformat(params))
        log.info("Fields: \n" + pformat(sid.fields))

    except SpilException as e:
        log.error("SpilException : {} --> {}".format(e, s))
        if reraise:
            raise e

    except Exception as e:
        log.error("Exception : {} --> {}".format(e, s))
        if reraise:
            raise e


def check_path_sids(sids, configs=[], reraise=True, replace=None):
    """
    Loop over test_sid.
    """

    log.info("Testing if example sids match the Sid config_name")

    if not sids:
        log.warning("No sids given, nothing to test.")
        return

    for i, s in enumerate(sids):
        log.info("*" * 75)
        log.info("----------------------------------------- {}".format(i))
        check_path_sid(s, configs=configs, reraise=reraise, replace=replace)


if __name__ == "__main__":

    from spil.util.log import setLevel, DEBUG, INFO

    setLevel(INFO)

    # from hamlet_scripts.example_sids import sids
    sids = []

    check_path_sids(sids)
