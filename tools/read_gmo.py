from formats.gmo import Gmo
import sys
import os

gmo = Gmo(open(sys.argv[1], 'rb').read())

mtl = open('test.mtl', 'w')
gmo.subfiles[0].write_mtl(mtl)
obj = open('test.obj', 'w')
gmo.subfiles[0].objects[0].write_obj(obj, 'test.mtl')
