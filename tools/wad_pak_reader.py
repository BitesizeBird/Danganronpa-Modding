import formats.wad as wad
import formats.pak as pak
import argparse
import sys

parser = argparse.ArgumentParser(description='.wad .pak lister')
parser.add_argument('input')
parser.add_argument('path')
parser.add_argument('indices', nargs='*', type=int)
args = vars(parser.parse_args())

indices = args['indices']

input = open(args['input'], 'rb')
wad_header = wad.WadHeader(input)

for file in wad_header.files:
    if file['path'] == args['path']:
        pak_header = pak.PakHeader(input, wad_header.header_size + file['offset'])
        for idx in indices:
            pak_header = pak.PakHeader(input, pak_header.base_offset + pak_header.offsets[idx])

        for offset in pak_header.offsets:
            str_offset = pak_header.base_offset + offset
            input.seek(str_offset)
            str_data = bytearray()
            
            in_ = input.read(2)
            assert in_ == b'\xff\xfe'
            in_ = input.read(2)
            while in_ != b'\0\0':
                str_data.extend(in_)
                in_ = input.read(2)

            print(repr(str_data.decode('utf-16-le')))
        sys.exit(0)
print("path not found :(")
