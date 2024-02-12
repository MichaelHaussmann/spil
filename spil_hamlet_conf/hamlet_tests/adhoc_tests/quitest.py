from resolva import Resolver

pat = {'asset_movie_file': '/home/mh/PycharmProjects/spil2/spil_hamlet_conf/data/testing/SPIL_PROJECTS/SERVER/PROJECTS/{project:(HAMLET|\*|\>)}/PROD/{type:(ASSETS|\*\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}/OUTPUT/{assettype:(char|location|prop|fx|\*|\>)}_{asset}_{task:(art|model|surface|rig|\*|\>)}_{state:(WORK|PUBLISH|\*|\>)}_{version:(v\d\d\d|\*|\>)}.{ext:(mp4|mov|avi|movie|\*|\>)}'}
r = Resolver("t", pat)

input = "/home/mh/PycharmProjects/spil2/spil_hamlet_conf/data/testing/SPIL_PROJECTS/SERVER/PROJECTS/*/PROD/ASSETS/char/claudius/rig/v001/OUTPUT/char_claudius_rig_WORK_v001.mp4"

result = r.resolve_one(input, "asset_movie_file")
print(result)