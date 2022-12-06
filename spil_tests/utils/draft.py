

sids = ['raj/a/char/juliet/low/design/v002/w/mp4', 'raj/a/char/juliet/low/design/v002']
    match_tests = ['*/*/**/v002/w/movie', '*/*/**/movie', '*/**/movie', 'hamlet/a,s/*/*/*/*/*']

    for sid in sids:
        for against in match_tests:
            print('{} U {} ? -> {}'.format(sid, against, Sid(sid).match(against)) )
    print()