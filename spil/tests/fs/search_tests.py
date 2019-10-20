from spil.libs.fs.fs import FS
from spil.libs.sid import Sid

if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('')
    info('Search Tests start')
    info('')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.fs_conf import search_sids

    for test in search_sids[0:]:

        search = Sid(test)

        if not search:
            info('Search not matching a sid, skipping : {}'.format(test))
            continue

        info('Search : {} ({})'.format(search, search.sidtype()))

        for sid in FS.find(search):
            # info('{} ({})'.format(sid, sid.sidtype()))
            info('\t\tFound {}'.format(sid))

        info(' '*10)
        info('*'*20)
