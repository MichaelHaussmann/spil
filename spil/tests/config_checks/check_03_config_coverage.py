"""
Test if the given Sid list covers all the templates.

This allows to make sure the configuration test is complete.

"""
from pprint import pformat

from spil import Sid

from spil.conf import sid_templates  # type: ignore

from spil.util.log import DEBUG, ERROR, get_logger
log = get_logger('tests')
log.setLevel(DEBUG)


def test_config_coverage(sids):

    all_types = set(sid_templates.keys())
    covered = set()
    remaining = all_types.copy()

    log.debug('- Testing coverage of given sids for sid_templates (sid_conf)...')

    for sid in sids:
        _sid = Sid(sid)
        if _sid.type in remaining:
            covered.add(_sid.type)
            log.debug(f"Covering: {_sid.type}")
            remaining.remove(_sid.type)
            if not remaining:
                break

    missing = remaining

    log.debug(f"Covered: {pformat(covered)}")

    if missing:
        log.warning(f"\tFAILED: Types not covered by given sids: {pformat(missing)}")
    else:
        log.info('\tOK: All types covered.')

    log.debug('done')


if __name__ == '__main__':

    sids = ["hamlet", "hamlet/a", "hamlet/a/char"]
    test_config_coverage(sids)
