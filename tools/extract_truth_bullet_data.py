import formats.wad as wad
import metadata
from metadata.truth_bullets import truth_bullets
import argparse
import toml

parser = argparse.ArgumentParser(description='extracts truth bullet data from dr2_data_us.wad')
parser.add_argument('input')
args = vars(parser.parse_args())

input = open(args['input'], 'rb')
wad_header = wad.WadHeader(input)

result = metadata.extract_from_metadata(wad_header, input, truth_bullets)
print(toml.dumps(result))
