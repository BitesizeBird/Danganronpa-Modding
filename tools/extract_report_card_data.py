import formats.wad as wad
import formats.pak as pak
from formats.helper import *
import argparse
import toml

parser = argparse.ArgumentParser(description='extracts report card data from dr2_data_us.wad')
parser.add_argument('input')
args = vars(parser.parse_args())

input = open(args['input'], 'rb')
wad_header = wad.WadHeader(input)

pak_offset = None
for file in wad_header.files:
    if file['path'] == 'Dr2/data/us/bin/bin_progress_font_l.pak':
        pak_offset = wad_header.header_size + file['offset']
assert pak_offset is not None

pak_header = pak.PakHeader(input, pak_offset)
print(len(pak_header.offsets))
pak_header = pak.PakHeader(input, pak_header.base_offset + pak_header.offsets[16])
print(len(pak_header.offsets))

report_card = {}

for i in range(16):
    data = []
    for j in range(8):
        offset = pak_header.base_offset + pak_header.offsets[16*j + i]
        input.seek(offset)
        value = read_string(input)
        data.append(value)

    report_card['{:02}'.format(i)] = {
            'name': data[0],
            'height': data[1],
            'weight': data[2],
            'chest': data[3],
            'blood_type': data[4],
            'birthday': data[5],
            'likes': data[6],
            'dislikes': data[7],
            }

print(toml.dumps(report_card))
