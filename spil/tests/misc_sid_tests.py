from spil.libs.sid import Sid
from spil.libs.util.log import setLevel, INFO, info, debug
from spil.conf.sid_conf import test_sids

if __name__ == '__main__':

    setLevel(INFO)
    #setLevel(DEBUG)  # In case of problems, use DEBUG mode

    sid = Sid('demo/s/010/0200/animation/*/001/w/ma')
    print(( sid + 'bla' ) )

    sid = Sid('demo/s/010/0200/layout/*/002/p')
    print( sid )

    sid = Sid('demo/s/010/0200')
    print( sid + 'layout' + '*' + '002' + 'p' )

    debug('Tests are in the tests.sid_tests module')

    sids = test_sids
    for sid in sids:  # sids[-1:]:
        info('')
        info('Testing {}'.format(sid))
        info('')
        sid = Sid(sid)
        if sid.basetype() == 'project':
            continue

        if sid.is_shot():
            info('Copy until Shot: {}'.format(sid.copy(until='shot')))
            info('As shot : {}'.format(sid.get_as('shot')) )
            info('As state : {}'.format(sid.get_as('state')) )
        new = sid.copy()
        new.set_defaults()
        info('With defaults {}'.format(new))
        info('Task : {}'.format(sid.get('task')) )
        info('Task : {}'.format(sid.task) )
        info('As Task : {}'.format(sid.get_as('task')) )
        info('With : {}'.format(sid.get_with(seq='99', version='valid')) )
        info('With : {}'.format(sid.get_with('task', value='layout')) )
        info('Parent : {}'.format(sid.parent()) )
        info('Parent, with defaults : {}'.format(sid.parent(set_default=True)))
        new = sid.parent(set_default=True)
        info('New dict : {}'.format(new.asdict()))
        info('')
        info('**********************************************************************************')
