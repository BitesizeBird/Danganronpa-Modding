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
pak8_header = pak.PakHeader(input, pak_header.base_offset + pak_header.offsets[8])
pak9_header = pak.PakHeader(input, pak_header.base_offset + pak_header.offsets[9])
pak16_header = pak.PakHeader(input, pak_header.base_offset + pak_header.offsets[16])

report_card = {}

for i in range(16):
    data = []
    for j in range(8): # misc data
        offset = pak16_header.base_offset + pak16_header.offsets[16*j + i]
        input.seek(offset)
        value = read_string(input)
        data.append(value)
    for j in range(3): # ultimate talent displays
        offset = pak8_header.base_offset + pak8_header.offsets[16*j + i]
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
            'ultimate': [
                data[8],
                data[9],
                data[10],
                ],
            }

    if i > 0:
        summaries = []
        for j in range(3): # fte blurbs
            offset = pak9_header.base_offset + pak9_header.offsets[3*i + j]
            input.seek(offset)
            value = read_string(input)
            summaries.append(value)

        report_card['{:02}'.format(i)]['fte_summaries'] = summaries

print(toml.dumps(report_card))
