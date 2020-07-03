import formats.wad as wad
import metadata
from metadata.presents import presents
import argparse

parser = argparse.ArgumentParser(description='extracts data from dr2_data_us.wad')
parser.add_argument('input')
parser.add_argument('output')
args = vars(parser.parse_args())

input = open(args['input'], 'rb')
wad_header = wad.WadHeader(input)

metadata.extract_all(wad_header, input, args['output'])
