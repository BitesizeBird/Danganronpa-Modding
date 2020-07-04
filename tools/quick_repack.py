import formats.wad as wad
import metadata
import argparse

parser = argparse.ArgumentParser(description='repacks previously extracted data')
parser.add_argument('input')
parser.add_argument('dr2_data')
parser.add_argument('dr2_data_us')
parser.add_argument('--prefix', default='')
args = vars(parser.parse_args())

dr2_data = wad.Wad(args['dr2_data'])
dr2_data_us = wad.Wad(args['dr2_data_us'])

wads = {
    'dr2_data': dr2_data,
    'dr2_data_us': dr2_data_us,
}

metadata.quick_repack(wads, args['input'], args['prefix'])
