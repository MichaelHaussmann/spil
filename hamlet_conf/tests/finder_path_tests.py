"""
This is work in progress.

"""

from spil import FindInPaths, Sid, FindInList, setLevel, FindInAll

from scripts.example_sids import sids  # type: ignore

search = 'hamlet/a/char/hamlet/rig/v001/p/*'
search = "hamlet/s/sq010/sh0030/*/*/p/*"
search = "hamlet/a/location/ramparts/rig/*/p"

print(Sid(search).path())

# finder = FindInPaths()
finder = FindInAll()
# finder2 = FindInList(sids)
from spil.util.log import setLevel, DEBUG, INFO, WARN
# setLevel(WARN)
setLevel(DEBUG)

print('*'*10)
for sid in finder.find(search):
    print(sid)
# print('*'*10)
# for sid in finder2.find(search):
#     print(sid)
# print('*'*10)
