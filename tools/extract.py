import formats.wad as wad
import metadata
from metadata.presents import presents
import argparse

parser = argparse.ArgumentParser(description='extracts data from dr2_data.wad and dr2_data_us.wad')
parser.add_argument('dr2_data')
parser.add_argument('dr2_data_us')
parser.add_argument('output')
parser.add_argument('--prefix', default='')
args = vars(parser.parse_args())

dr2_data = wad.Wad(args['dr2_data'])
dr2_data_us = wad.Wad(args['dr2_data_us'])


wads = {
    'dr2_data': dr2_data,
    'dr2_data_us': dr2_data_us,
}

metadata.extract(wads, args['output'], args['prefix'])
