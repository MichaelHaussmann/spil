from spil.libs.fs.fs import FS
from spil.libs.sid import Sid

if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('')
    info('Search Tests start')
    info('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.sid_conf import test_sids

    for test in test_sids[0:]:

        sid = Sid(test).get_with('subtask', '*')  # FIXME
        info('Sid : {}'.format(sid))

        for sid in FS.get_children(sid):
            # info('{} ({})'.format(sid, sid.sidtype()))
            info('\t\tChild {}'.format(sid))

        search = Sid(test).get_with('task', '*').get_with('state', '*').get_with('version', '*').get_with('subtask', '*')

        if not search:
            info('Search not matching a sid, skipping : {}'.format(test))
            continue

        info('Search : {} ({})'.format(search, search.sidtype()))

        for sid in FS.find(search):
            # info('{} ({})'.format(sid, sid.sidtype()))
            info('\t\tFound {}'.format(sid))

        info(' '*10)
        info('*'*20)
