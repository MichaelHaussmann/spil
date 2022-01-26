from spil.util.log import DEBUG, ERROR, get_logger
from spil import Sid, SpilException, FS, Data
from pprint import pformat

log = get_logger('spil_tests')
log.setLevel(DEBUG)


def test_sid(s, reraise=True):
    """
    Little test protocol for the Sid.

    Only major or unexpected problems trigger exceptions.
    Most configuration problems trigger log warnings.

    If reraise is True, exceptions are reraised, otherwise there are logged.

    """

    log.info('Testing: "{}"'.format(s))
    sid = Sid(s)
    log.info('Instanced: "{}"'.format(sid.full_string))

    if not s.count('?'):  # Asset works only without URI part
        assert str(sid) == s
    assert sid == eval(repr(sid))

    try:
        if not sid.type:
            log.error('Sid "{}" not typed, skipping'.format(sid))
            return

        assert sid == Sid(sid.get('project') + '?' + sid.get_uri()), 'Sid URI assertion pb : {}'.format(Sid(sid.get('project') + '?' + sid.get_uri()))

        test_search(sid)

        key = sid.keytype
        parent_key = sid.parent.keytype

        if not sid.type == 'project':
            if sid.parent and sid.get_as(parent_key):
                if not sid.parent == sid.get_as(parent_key):
                    log.warn('Sid "{}" parent problem'.format(sid))
            else:
                log.warn('Sid "{}" has not parent ?'.format(sid))

        if not sid.get_last(key):
            log.warn('Sid "{}" does not return get_last("{}") - probably bad.'.format(sid, key))

        path = sid.path
        if path:
            try:
                assert sid == Sid(path=sid.path)
                log.info('Passed : sid == Sid(path=sid.path) ')
            except AssertionError:
                msg = 'Sid path is ambiguous.\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\n'.format(sid, sid.path,
                                                                                                       Sid(path=sid.path))
                log.warn(msg)
            try:
                assert sid.path == Sid(path=sid.path).path
                log.info('Passed : sid.path == Sid(path=sid.path).path ')
            except AssertionError:
                msg = 'Sid path is ambiguous.\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\nSid(path=sid.path).path: {}'.format(
                    sid,
                    sid.path,
                    Sid(path=sid.path),
                    Sid(path=sid.path).path)
                log.warn(msg)
        else:
            log.error('Sid "{}" has no path.'.format(sid))

        params = {'parent': sid.parent,
                  'grand_parent': sid.parent.parent,
                  'basetype': sid.basetype,
                  'keytype': sid.keytype,
                  'path': sid.path,
                  'exists': sid.exists(),
                  'is_leaf': sid.is_leaf(),
                  'len': len(sid),
                  'get_last': sid.get_last(),
                  'get_last (version)': sid.get_last('version'),
                  'get_next': sid.get_next('version'),
                  'get_new': sid.get_new('version'),
                  'type': sid.type,
                  'full_string': sid.full_string,
                  'string': sid.string,
                  'uri': sid.get_uri(),
                  }

        log.info('Params: \n' + pformat(params))
        log.info('Data: \n' + pformat(sid.data))

    except SpilException as e:
        log.error('SpilException : {} --> {}'.format(e, s))
        if reraise:
            raise e

    except Exception as e:
        log.error('Exception : {} --> {}'.format(e, s))
        if reraise:
            raise e


def test_sids(sids, reraise=True):
    """
    Loop over test_sid.
    """

    log.info('Testing if example sids match the Sid config')

    if not sids:
        log.warn('No sids given, nothing to test.')
        return

    for i, s in enumerate(sids):
        log.debug('---------------- {}'.format(i))
        test_sid(s, reraise=reraise)


def test_search(sid):
    """
    Runs a search on the given Sid.
    If the Sid exists on the system, the search result should equal the search.
    This test is called by test_sid.
    """

    sid = Sid(sid)

    found = FS().get_one(sid)
    log.info('{} ----> FS() --->  {}'.format(sid, found))
    #assert (sid == found)

    found = Data().get_one(sid)
    log.info('{} ----> Data() --->  {}'.format(sid, found))
    #assert(sid == found)


if __name__ == '__main__':

    from spil.util.log import setLevel, ERROR, DEBUG
    setLevel(ERROR)

    sids = ['FTOT/S/SQ0001/SH0010', 'ARM/R', 'foo']

    test_sids(sids)

