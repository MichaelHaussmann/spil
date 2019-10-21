from spil.libs.sid import Sid

if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, warn
    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    print('')
    print('Tests start')
    print('')

    from spil.conf.sid_conf import test_sids

    asset_sid = test_sids[0]
    sid = Sid(asset_sid)

    print(sid)

    print('Acess to "values"')
    if sid.is_asset:
        print(sid.cat)
        print(sid.name)
    elif sid.is_shot:
        print(sid.seq)
        print(sid.shot)
    print(sid.version)
    print(sid.task)
    print(sid.get('task'))
    print(sid.path)
    print('')

    print('Changing the Sid')
    print(sid.get_as('task'))
    print(sid.get_as('task').parent())
    print(sid.get_with('task', 'surfacing'))
    print(sid.get_with(task='setup', state='w'))
    print('')

    print('Utilities')

    print(sid.get_as('subtask').parent().last_key())  # 'task'
    print(sid.get_as('name').has_a('task'))  # sid until name does not have a task
    print(len(sid))  # the number of valid values
    print(len(sid.get_as('task')))
    print('')

    print('Iterating over keys - always all the keys')
    for key in sid.keys:
        print('\t' + key)
    print('')

    print('Iterate over values - only valid (or optional) values')
    for value in sid.get_as('task'):
        print('\t' + value)
    print('')

    print('Types & dict')
    print(sid.sidtype())
    print(sid.basetype())
    print(sid.endtype())
    print(sid.asdict())
    print('')


