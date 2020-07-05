import sys
import formats.tga as tga
import formats.wad
import png

wad = wad.Wad(sys.argv[1])
output = open(sys.argv[2], 'wb')

Tga('', '', '', [0]).extract_to({'': wad}, output)

output.close()
