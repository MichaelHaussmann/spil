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


def check_typed_sid(s, reraise=True, replace=None):
    """
    Test protocol for the Typed Sid.

    Tests only core feature, without delegation (to Finders or Getters).
    Does not include path tests.

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
    log.info('Instanced: "{}"'.format(sid.uri))

    if not s.count("?"):  # Assert works only without Query part
        assert str(sid) == s
    assert sid == eval(repr(sid))

    try:
        if not sid.type:
            log.error('Sid "{}" not typed, skipping'.format(sid))
            return

        params = {
            "parent": sid.parent,
            "grand_parent": sid.parent.parent,
            "basetype": sid.basetype,
            "keytype": sid.keytype,
            "len": len(sid),
            "type": sid.type,
            "uri": sid.uri,
            "string": sid.string,
            "query": sid.as_query(),
            "is_search": sid.is_search(),
        }

        log.info("Params: \n" + pformat(params))
        log.info("Fields: \n" + pformat(sid.fields))

        # todo: create a Search Sid from current Sid
        """
        search_sid = sid.get_with(key=sid.keytype, value='*')
        match = True  # sid.match(search_sid)
        if not match:
            log.warning('No match "{}" <-> "{}". This is not normal'.format(sid, search_sid))
        """

        parent_key = sid.parent.keytype
        if not sid.type == "project":
            if sid.parent and sid.get_as(parent_key):
                if not sid.parent == sid.get_as(parent_key):
                    log.warning('Sid "{}" parent problem'.format(sid))
            else:
                log.warning('Sid "{}" has not parent ?'.format(sid))

        assert sid == Sid(
            sid.get("project") + "?" + sid.as_query()
        ), "Sid Query assertion pb : {}".format(Sid(sid.get("project") + "?" + sid.get_query()))

        assert sid == Sid(
            sid.get("project") + "?" + sid.as_query()
        ), "Sid Query assertion pb : {}".format(Sid(sid.get("project") + "?" + sid.as_query()))
        log.info('Passed "Query": sid == Sid(sid.get("project")) + "?" + sid.get_query() ')

        if not sid.parent:
            log.warning("Sid {} has no valid parent (got: {}).".format(sid, sid.parent))
        elif sid == sid.parent:
            log.info("Sid is a root (has no parent).")
        else:
            assert sid == sid.parent / sid.get(sid.keytype)
            log.info('Passed "parent": sid == sid.parent / sid.get(sid.keytype) ')

    except SpilException as e:
        log.error("SpilException : {} --> {}".format(e, s))
        if reraise:
            raise e

    except Exception as e:
        log.error("Exception : {} --> {}".format(e, s))
        if reraise:
            raise e


def check_typed_sids(sids, reraise=True, replace=None):
    """
    Loop over core_test_sid.
    """

    log.info("Testing if example sids match the Sid config_name")

    if not sids:
        log.warning("No sids given, nothing to test.")
        return

    for i, s in enumerate(sids):
        log.info("*" * 75)
        log.info("----------------------------------------- {}".format(i))
        check_typed_sid(s, reraise=reraise, replace=replace)


if __name__ == "__main__":

    from spil.util.log import setLevel, DEBUG, INFO

    setLevel(INFO)

    # from hamlet_scripts.example_sids import sids
    sids = []

    check_typed_sids(sids)
