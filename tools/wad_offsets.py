import formats.wad as wad
import sys
import json
import pprint

wad = wad.Wad(sys.argv[1])
offsets = [[0, '<header>']]

for path, file in wad.files.items():
    offsets.append([file[0], path])

offsets.sort(key=lambda l: l[0])
for i in range(len(offsets)-1):
    assert offsets[i][0] < offsets[i+1][0]
print(json.dumps(offsets))
