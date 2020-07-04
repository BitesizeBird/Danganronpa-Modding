import sys
import formats.tga as tga
import png

input = png.Reader(sys.argv[1])
output = open(sys.argv[2], 'wb')
width, height, rows, info = input.read()
tga.write_tga(output, info['palette'], list(rows))
