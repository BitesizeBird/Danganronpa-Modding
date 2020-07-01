import formats.wad
import argparse

parser = argparse.ArgumentParser(description='.wad file updater')
parser.add_argument('input-wad')
parser.add_argument('filename-to-update')
parser.add_argument('new-file')
args = vars(parser.parse_args())

wad = formats.wad.Wad()
wad.read(args['input-wad'])

new_file = open(args['new-file'], 'rb').read()

wad.update_file(args['input-wad'], args['filename-to-update'], new_file)
