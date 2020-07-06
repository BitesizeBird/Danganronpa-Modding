import formats.lin as lin
import formats.wad as wad
import sys

wad = wad.Wad(sys.argv[1])
lin = lin.LinScript.read_from(wad, sys.argv[2])
