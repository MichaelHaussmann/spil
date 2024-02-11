from spil import FindInPaths, Sid

finder = FindInPaths("server")

search = 'hamlet/a/*/claudius/rig/*/w/*'
print('*'*50)
for f in finder.find(search, as_sid=False):
    print(f)
print('*'*50)
#
# for f in finder.find(search):
#     print(f)
# print('*'*50)

