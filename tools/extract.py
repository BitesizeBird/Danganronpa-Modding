import formats.wad as wad
import metadata
from metadata.presents import presents
import argparse

parser = argparse.ArgumentParser(description='extracts data from dr2_data.wad and dr2_data_us.wad')
parser.add_argument('dr2_data')
parser.add_argument('dr2_data_us')
parser.add_argument('output')
args = vars(parser.parse_args())

data = open(args['dr2_data'], 'rb')
data_header = wad.WadHeader(data)

data_us = open(args['dr2_data_us'], 'rb')
data_us_header = wad.WadHeader(data_us)

wads = {
    'dr2_data': [data, data_header],
    'dr2_data_us': [data_us, data_us_header],
}

metadata.extract_all(wads, args['output'])
