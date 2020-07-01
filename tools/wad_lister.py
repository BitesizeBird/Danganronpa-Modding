import formats.wad
import argparse

parser = argparse.ArgumentParser(description='.wad file lister')
parser.add_argument('input')
args = vars(parser.parse_args())

wad = formats.wad.Wad()
wad.read(args['input'])

for filename, metadata in wad.files.items():
    print(filename, metadata)
print('=====')
for dirname, _ in wad.dirs.items():
    print(dirname)
