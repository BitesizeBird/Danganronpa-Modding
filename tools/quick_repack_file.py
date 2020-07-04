import formats.wad as wad
import metadata
import argparse

parser = argparse.ArgumentParser(description='quickly replaces a file in a wad')
parser.add_argument('file')
parser.add_argument('wad')
parser.add_argument('path')
args = vars(parser.parse_args())

wad = wad.Wad(args['wad'])

with open(args['file'], 'rb') as f:
    new_data = f.read()

wad.update_file(args['path'], new_data)
