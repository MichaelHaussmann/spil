from spil.util.log import debug, setLevel, INFO, DEBUG, info, ERROR, warn, error
from spil import Sid, SpilException, FS, Data
from pprint import pprint, pformat


def test_sid(s, reraise=True):

    print('Testing: "{}"'.format(s))
    sid = Sid(s)
    print('Instanced: "{}"'.format(sid.full_string))

    if not s.count('?'):  # Asset works only without URI part
        assert str(sid) == s
    assert sid == eval(repr(sid))

    try:
        if not sid.type:
            warn('Sid "{}" not typed, skipping'.format(sid))
            return

        assert sid == Sid(sid.get('project') + '?' + sid.get_uri()), 'Sid URI assertion pb : {}'.format(Sid(sid.get('project') + '?' + sid.get_uri()))

        test_search(sid)

        key = sid.keytype
        parent_key = sid.parent.keytype

        if not sid.type == 'project':
            if sid.parent and sid.get_as(parent_key):
                if not sid.parent == sid.get_as(parent_key):
                    warn('Sid "{}" parent problem'.format(sid))
            else:
                warn('Sid "{}" has not parent ?'.format(sid))

        if not sid.get_last(key):
            print('Sid "{}" does not return get_last("{}") - probably bad.'.format(sid, key))

        path = sid.path
        if path:
            try:
                assert sid == Sid(path=sid.path)
                print('Passed : sid == Sid(path=sid.path) ')
            except AssertionError:
                msg = 'Sid path is ambiguous.\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\n'.format(sid, sid.path,
                                                                                                       Sid(path=sid.path))
                print(msg)
            try:
                assert sid.path == Sid(path=sid.path).path
                print('Passed : sid.path == Sid(path=sid.path).path ')
            except AssertionError:
                msg = 'Sid path is ambiguous.\nsid: {}\nsid.path: {}\nSid(path=sid.path): {}\nSid(path=sid.path).path: {}'.format(
                    sid,
                    sid.path,
                    Sid(path=sid.path),
                    Sid(path=sid.path).path)
                print(msg)
        else:
            print('Sid "{}" has no path.'.format(sid))

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

        pprint(params)
        pprint(sid.data)

    except SpilException as e:
        error('SpilException : {} --> {}'.format(e, s))
        if reraise:
            raise e

    except Exception as e:
        error('Exception : {} --> {}'.format(e, s))
        if reraise:
            raise e


def test_sids(sids, reraise=True):

    info('Testing if example sids match the Sid config')

    if not sids:
        warn('No sids given, nothing to test.')
        return

    for i, s in enumerate(sids):
        print('---------------- {}'.format(i))
        test_sid(s, reraise=reraise)


def test_search(sid):

    sid = Sid(sid)

    found = FS().get_one(sid)
    print('{} ----> FS() --->  {}'.format(sid, found))
    #assert (sid == found)

    found = Data().get_one(sid)
    print('{} ----> Data() --->  {}'.format(sid, found))
    #assert(sid == found)


