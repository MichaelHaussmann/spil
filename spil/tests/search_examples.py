from spil.libs.fs.fs import FS
from spil.libs.sid import Sid

if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, warn
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    print('')
    print('Tests start - Please init files for this to work')
    print('')

    from spil.conf.sid_conf import test_sids

    asset_sid = test_sids[0]
    sid = Sid(asset_sid)
    print(sid)
    print('')

    print('Get all characters (children of cat)')
    for asset in FS.get_children(sid.get_as('cat')):
        print(asset)
    print('')

    print('Get all tasks (children of asset name)')
    for asset in FS.get_children(sid.get_as('name')):
        print(asset)
    print('')

    print('Get by search sid : all tasks')
    search_sid = sid.get_with(name='*', task='*', cat='*').get_as('task')
    for asset in FS.find(search_sid):
        print(asset)
    print('')

    print('Get by search sid : all tasks for the given asset')
    search_sid = sid.get_with(task='*', cat='*').get_as('task')
    for asset in FS.find(search_sid):
        print(asset)
    print('')

    print('Get by search sid : all assets of cat "fx" in project demo')
    search_sid = Sid('demo/a/fx/*')
    for asset in FS.find(search_sid):
        print(asset)
    print('')

    print('Get by search sid : all "shots" in project demo')
    search_sid = Sid('demo/s/*/*')
    for sid in FS.find(search_sid):
        print(sid)
    print('')

    # FS.get_children(sid.get_as('project')) FIXME : doesn't work