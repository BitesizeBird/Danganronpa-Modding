import formats.pak as pak
from formats.helper import read_string

class PakString:
    def __init__(self, wad_name, pak_path, pak_indices):
        self.wad_name = wad_name
        self.pak_path = pak_path
        self.pak_indices = pak_indices

    # assumes the file refers to self.wad_name
    def extract_string(self, wads):
        [wad, wad_header] = wads[self.wad_name]

        offset = wad_header.header_size + next(entry['offset'] for entry in wad_header.files if entry['path'] == self.pak_path)

        for index in self.pak_indices:
            pak_header = pak.PakHeader(wad, offset)
            offset = pak_header.base_offset + pak_header.offsets[index]

        wad.seek(offset)
        value = read_string(wad)
        return value

import tempfile
_tmp_tga = tempfile.NamedTemporaryFile(suffix='.tga', mode='wb')
class Tga:
    def __init__(self, wad_name, path):
        self.wad_name = wad_name
        self.path = path

    def extract_to(self, wads, output):
        import formats.tga
        import png
        import io
        [wad, wad_header] = wads[self.wad_name]

        entry = next(entry for entry in wad_header.files if entry['path'] == self.path)
        offset = wad_header.header_size + entry['offset']
        size = entry['size']

        (color_map, pixel_data, width, height) = formats.tga.read_tga(wad, offset)
        w = png.Writer(width, height, palette=color_map)
        w.write(output, pixel_data)

# assumes there is only dr2_data_us.wad
def extract_from_metadata(wads, meta):
    if isinstance(meta, PakString):
        return meta.extract_string(wads)
    elif isinstance(meta, list):
        return [extract_from_metadata(wads, v) for v in meta]
    elif isinstance(meta, dict):
        return {k: extract_from_metadata(wads, v) for k, v in meta.items()}
    else:
        raise ValueError

def extract_all(wads, outdir):
    import os
    import toml

    for fname, meta in files.items():
        fpath = os.path.join(outdir, fname)
        print('writing {}'.format(fpath))

        fdir = os.path.dirname(fpath)
        if not os.path.exists(fdir): os.makedirs(fdir)

        if fname.endswith('.toml'):
            file = open(fpath, 'w')
            toml.dump(extract_from_metadata(wads, meta), file)
        else:
            file = open(fpath, 'wb')
            meta.extract_to(wads, file)
        file.close()

import metadata.report_card
import metadata.presents
import metadata.truth_bullets
import metadata.backgrounds

files = {
        'report_card.toml': report_card.report_card,
        'presents.toml': presents.presents,
        'truth_bullets.toml': truth_bullets.truth_bullets,
}

presents.add_files(files)
backgrounds.add_files(files)
