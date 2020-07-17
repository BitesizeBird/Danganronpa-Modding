from formats.gmo import Gmo
import sys
import os

gmo = Gmo(open(sys.argv[1], 'rb').read())

for i, subfile in enumerate(gmo.subfiles):
    mtl = open('test{}.mtl'.format(i), 'w')
    gmo.subfiles[i].write_mtl(mtl)
    for j, object in enumerate(subfile.objects):
        obj = open('test{}_{}.obj'.format(i, j), 'w')
        gmo.subfiles[i].objects[j].write_obj(obj, 'test{}.mtl'.format(i))
