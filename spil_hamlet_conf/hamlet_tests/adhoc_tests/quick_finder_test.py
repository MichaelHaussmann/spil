"""
Debug for specific search results.

hamlet/a/*/claudius/rig/v001/*/*
hamlet/a/*/claudius/rig/*/w/*
hamlet/*/char/claudius/*/v001/w/*

"""
import spil
from hamlet_scripts.example_sids import sids  # type: ignore
from spil import FindInList, FindInPaths

# finder = FindInList(sids)
finder = FindInPaths("server")

search = 'hamlet/a/*/claudius/rig/*/w/*'
# search = 'hamlet/*/char/claudius/*/v001/w/*'
# search = 'hamlet/a/*/claudius/rig/*/w/**'

for i in range(1):
    print('*'*50)
    for f in finder.find(search):
        print(f)
    print('*'*50)
#
# for f in finder.find(search):
#     print(f)
# print('*'*50)

