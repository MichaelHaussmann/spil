# -*- coding: utf-8 -*-
"""






"""


from spil.conf.sid_conf import test_sids
from spil.libs.sid import Sid

from spil.libs.util.log import setLevel, INFO

setLevel(INFO)
# setLevel(DEBUG)  # In case of problems, use DEBUG mode

for test in test_sids[:]:
    # print( test
    sid = Sid(test)
    print( sid )
    print( sid.copy() )

    for index, value in enumerate(sid):
        print( sid.keys[index], '-->', value )
    print( '-' * 5 )

    # Copy
    for part in sid.keys:
        copied = sid.copy(until=part)
        if copied:
            print( 'until', part, '-->', copied, copied.last_key())

    # get as
    for part in sid.keys:
        new = sid.get_as(part)
        if new:
            print( 'As', part, '-->', new, new.last_key())

    # len
    while len(sid):
        print( 'sid : ', sid, 'len', len(sid), sid.last_key()) # , repr(sid)
        print( 'sid : ', sid.get_as(sid.last_key()))
        print( '-'*5 )
        if sid.parent() == sid:
            break
        sid = sid.parent()

    print( '*'*20 )



