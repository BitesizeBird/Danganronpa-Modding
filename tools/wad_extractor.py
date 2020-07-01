import formats.wad
import argparse

parser = argparse.ArgumentParser(description='.wad file extractor')
parser.add_argument('input')
parser.add_argument('filename')
parser.add_argument('output')
args = vars(parser.parse_args())

wad = formats.wad.Wad()
wad.read(args['input'])
buffer = wad.read_file(args['input'], args['filename'])

file = open(args['output'], 'wb')
file.write(buffer)
