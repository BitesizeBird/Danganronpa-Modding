import formats.wad
import argparse

parser = argparse.ArgumentParser(description='.wad file lister')
parser.add_argument('input')
args = vars(parser.parse_args())

header = formats.wad.WadHeader(open(args['input'], 'rb'))
print(header.header_size)

for file in header.files:
    print(file)
print('=====')
for dir in header.dirs:
    print(dir['path'])
