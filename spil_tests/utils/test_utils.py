# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
from spil.util.log import DEBUG, ERROR, get_logger
from spil import Sid, SpilException, FS, Data
from pprint import pformat

log = get_logger("spil_tests")
log.setLevel(DEBUG)


def test_sid(s, reraise=True, replace=None, from_search=None):
    """
    Little test protocol for the Sid.

    Only major or unexpected problems trigger exceptions.
    Most configuration problems trigger log warnings.

    If reraise is True, exceptions are reraised, otherwise there are logged.
    replace can be a tuple that is used for string replacement on the tested Sid.

    from_search allows to pass a search string, to test the match.
    """
    s = str(s)
    if replace:
        s = s.replace(*replace)

    log.info('Testing: "{}"'.format(s))
    sid = Sid(s)
    log.info('Instanced: "{}"'.format(sid.full_string))

    if not s.count("?"):  # Asset works only without URI part
        assert str(sid) == s
    assert sid == eval(repr(sid))

    try:
        if not sid.type:
            log.error('Sid "{}" not typed, skipping'.format(sid))
            return

        test_search(sid)

        if from_search:
            match = sid.match(from_search)
            if not match:
                log.warning('No match "{}" <-> "{}". This is not normal'.format(sid, from_search))

        key = sid.keytype
        parent_key = sid.parent.keytype

        if not sid.type == "project":
            if sid.parent and sid.get_as(parent_key):
                if not sid.parent == sid.get_as(parent_key):
                    log.warning('Sid "{}" parent problem'.format(sid))
            else:
                log.warning('Sid "{}" has not parent ?'.format(sid))

        if not sid.get_last(key):
            log.warning('Sid "{}" does not return get_last("{}") - probably bad.'.format(sid, key))

        assert sid == Sid(
            sid.get("project") + "?" + sid.get_uri()
        ), "Sid URI assertion pb : {}".format(Sid(sid.get("project") + "?" + sid.get_uri()))
        log.info('Passed "URI": sid == Sid(sid.get("project") + "?" + sid.get_uri() ')

        if not sid.parent:
            log.warning("Sid {} has no valid parent (got: {}).".format(sid, sid.parent))
        elif sid == sid.parent:
            log.info("Sid is a root (has no parent).")
        else:
            assert sid == sid.parent / sid.get(sid.keytype)
            log.info('Passed "parent": sid == sid.parent / sid.get(sid.keytype) ')

        path = sid.path
        if path:
            try:
                assert sid == Sid(path=sid.path)
                log.info("Passed : sid == Sid(path=sid.path) ")
            except AssertionError:
                msg = "Sid path is ambiguous. {}\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\n".format(
                    "(Sid is a search, this may be normal)." if sid.is_search() else "",
                    sid, sid.path, Sid(path=sid.path)
                )
                log.warning(msg)
            try:
                assert sid.path == Sid(path=sid.path).path
                log.info("Passed : sid.path == Sid(path=sid.path).path ")
            except AssertionError:
                msg = "Sid path is ambiguous. {}\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\nSid(path=sid.path).path: {}".format(
                    "(Sid is a search, this may be normal)." if sid.is_search() else "",
                    sid, sid.path, Sid(path=sid.path), Sid(path=sid.path).path
                )
                log.warning(msg)
        else:
            log.error('Sid "{}" has no path.'.format(sid))

        params = {
            "parent": sid.parent,
            "grand_parent": sid.parent.parent,
            "basetype": sid.basetype,
            "keytype": sid.keytype,
            "path": sid.path,
            "exists": sid.exists(),
            "is_leaf": sid.is_leaf(),
            "len": len(sid),
            "get_last": sid.get_last(),
            "get_last (version)": sid.get_last("version"),
            "get_next": sid.get_next("version"),
            "get_new": sid.get_new("version"),
            "type": sid.type,
            "full_string": sid.full_string,
            "string": sid.string,
            "uri": sid.get_uri(),
            "is_search": sid.is_search(),
        }

        log.info("Params: \n" + pformat(params))
        log.info("Data: \n" + pformat(sid.data))

    except SpilException as e:
        log.error("SpilException : {} --> {}".format(e, s))
        if reraise:
            raise e

    except Exception as e:
        log.error("Exception : {} --> {}".format(e, s))
        if reraise:
            raise e


def test_sids(sids, reraise=True, replace=None):
    """
    Loop over test_sid.
    """

    log.info("Testing if example sids match the Sid config")

    if not sids:
        log.warning("No sids given, nothing to test.")
        return

    for i, s in enumerate(sids):
        log.debug("---------------- {}".format(i))
        test_sid(s, reraise=reraise, replace=replace)


def test_search(sid):
    """
    Runs a search on the given Sid.
    If the Sid exists on the system, the search result should equal the search.
    This test is called by test_sid.
    """

    sid = Sid(sid)

    found = FS().get_one(sid)
    log.info("{} ----> FS() --->  {}".format(sid, found))
    # assert (sid == found)

    found = Data().get_one(sid)
    log.info("{} ----> Data() --->  {}".format(sid, found))
    # assert(sid == found)


if __name__ == "__main__":

    from spil.util.log import setLevel, ERROR, DEBUG

    setLevel(ERROR)

    sids = ["FTOT/*", "FTOT/A","FTOT/S/SQ0001/SH0010"]  # , "FTOT/R",  "foo"]

    test_sids(sids)
