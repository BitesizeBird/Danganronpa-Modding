import formats.pak as pak
from formats.helper import read_string

class PakString:
    def __init__(self, wad_name, pak_path, pak_indices):
        self.wad_name = wad_name
        self.pak_path = pak_path
        self.pak_indices = pak_indices

    def extract_string(self, wads):
        wad = wads[self.wad_name]

        offset = wad.files[self.pak_path][0]

        for index in self.pak_indices:
            pak_header = pak.PakHeader(wad.file, offset)
            offset = pak_header.base_offset + pak_header.offsets[index]

        wad.file.seek(offset)
        value = read_string(wad.file)
        return value

class Tga:
    def __init__(self, wad_name, path):
        self.wad_name = wad_name
        self.path = path

    def extract_to(self, wads, output):
        import formats.tga
        import png
        import io
        wad = wads[self.wad_name]

        entry = wad.files[self.path]
        offset = entry[0]
        size = entry[1]

        color_map, pixel_data = formats.tga.read_tga(wad.file, offset)
        w = png.Writer(len(pixel_data[0]), len(pixel_data), palette=color_map)
        w.write(output, pixel_data)

    def repack(self, wads, input):
        import formats.tga
        import png
        import io
        wad = wads[self.wad_name]

        input = png.Reader(input)
        output = io.BytesIO()
        _, _, rows, info = input.read()
        formats.tga.write_tga(output, info['palette'], list(rows))

        return output.getbuffer()

def extract_from_metadata(wads, meta):
    if isinstance(meta, PakString):
        return meta.extract_string(wads)
    elif isinstance(meta, list):
        return [extract_from_metadata(wads, v) for v in meta]
    elif isinstance(meta, dict):
        return {k: extract_from_metadata(wads, v) for k, v in meta.items()}
    else:
        raise ValueError

def extract(wads, outdir, prefix=''):
    import os
    import toml

    if not os.path.exists(outdir): os.makedirs(outdir)

    # read sync file, if it exists
    sync_path = os.path.join(outdir, '.sync.toml')
    if not os.path.exists(sync_path): open(sync_path, 'a').close()
    sync_data = toml.load(sync_path)

    for fname, meta in files.items():
        if not fname.startswith(prefix): continue

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
        sync_data[fname] = os.path.getmtime(fpath)

    # rewrite sync file
    print('writing sync file')
    sync_file = open(sync_path, 'w')
    toml.dump(sync_data, sync_file)
    sync_file.close()

import metadata.report_card
import metadata.presents
import metadata.truth_bullets
import metadata.backgrounds
import metadata.sprites

files = {
        'report_card.toml': report_card.report_card,
        'presents.toml': presents.presents,
        'truth_bullets.toml': truth_bullets.truth_bullets,
}

report_card.add_files(files)
presents.add_files(files)
backgrounds.add_files(files)
sprites.add_files(files)

_file_to_meta = {}
