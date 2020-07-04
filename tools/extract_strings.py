import sys
import pprint
import formats.wad as wad
import formats.pak as pak

wad = wad.Wad(sys.argv[1])
pak_header = pak.PakHeader(wad.file, wad.files[sys.argv[2]][0])
strings = pak_header.extract_strings(wad.file)

pprint.pprint(strings)
