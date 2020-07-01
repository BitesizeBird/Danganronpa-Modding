import formats.wad
import argparse

parser = argparse.ArgumentParser(description='.wad file lister')
parser.add_argument('input')
args = vars(parser.parse_args())

with open(args['input'], 'rb') as file:
    wad = formats.wad.Wad()
    wad.read(file)

    for filename in wad.files:
        print(filename)
    print('=====')
    for dirname in wad.dirs:
        print(dirname)
