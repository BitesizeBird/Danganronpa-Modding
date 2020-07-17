import formats.wad as wad
import formats.pak as pak
import formats.tga as tga
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='.pak tga reader')
parser.add_argument('input')
#parser.add_argument('path')
parser.add_argument('indices', nargs='*', type=int)
parser.add_argument('output')
args = vars(parser.parse_args())

#wad = wad.Wad(args['input'])
outdir = args['output']
if not os.path.exists(outdir): os.makedirs(outdir)
indices = args['indices']

#entry = wad.files[args['path']]
file = open(args['input'], 'rb')
#offset = entry[0]
offset = 0
for idx in indices:
    pak_header = pak.PakHeader(file, offset)
    offset = pak_header.base_offset + pak_header.offsets[idx]

pak_header = pak.PakHeader(file, offset)
for i, offset in enumerate(pak_header.offsets):
    begin = pak_header.base_offset + offset
    #tga.read_tga(wad.file, begin)
    #end = wad.file.tell()
    end = pak_header.base_offset + pak_header.offsets[i+1] if i < len(pak_header.offsets)-1 else os.path.getsize(args['input'])

    file.seek(begin)
    data = file.read(end - begin)

    out = open(os.path.join(outdir, '{:03}'.format(i)), 'wb')
    out.write(data)
    out.close()
