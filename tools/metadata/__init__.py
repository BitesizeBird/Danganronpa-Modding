import formats.pak as pak
from formats.helper import read_string

# refers to a zero terminated, utf-16-le string nested inside a .pak
class String:
    def __init__(self, wad_name, path, indices):
        self.wad_name = wad_name
        self.path = path
        self.indices = indices

    def extract(self, wads):
        wad = wads[self.wad_name]

        offset = wad.files[self.path][0]

        for index in self.indices:
            pak_header = pak.PakHeader(wad.file, offset)
            offset = pak_header.base_offset + pak_header.offsets[index]

        wad.file.seek(offset)
        value = read_string(wad.file)
        return value

# refers to an entire pak of the latter (serialized as a map)
class Strings:
    def __init__(self, wad_name, path, indices, key_width):
        self.wad_name = wad_name
        self.path = path
        self.indices = indices
        self.key_width = key_width

    def extract(self, wads):
        wad = wads[self.wad_name]
        offset = wad.files[self.path][0]

        pak_header = pak.PakHeader(wad.file, offset)
        for index in self.indices:
            offset = pak_header.base_offset + pak_header.offsets[index]
            pak_header = pak.PakHeader(wad.file, offset)

        values = {}
        for i, offset in enumerate(pak_header.offsets):
            wad.file.seek(pak_header.base_offset + offset)
            values[str(i).zfill(self.key_width)] = read_string(wad.file)
        return values

# refers to a targa image file either on its own or in the top level of a .pak
class Tga:
    def __init__(self, wad_name, path, indices=[]):
        self.wad_name = wad_name
        self.path = path
        self.indices = indices

    def extract_to(self, wads, output):
        import formats.tga
        import png
        import io
        wad = wads[self.wad_name]

        entry = wad.files[self.path]
        offset = entry[0]
        size = entry[1]

        for index in self.indices:
            pak_header = pak.PakHeader(wad.file, offset)
            offset = pak_header.base_offset + pak_header.offsets[index]

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
    if isinstance(meta, String) or isinstance(meta, Strings):
        return meta.extract(wads)
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


def quick_repack(wads, indir, prefix=''):
    import io
    import os
    import toml

    # read sync file
    sync_path = os.path.join(indir, '.sync.toml')
    if not os.path.exists(sync_path): open(sync_path, 'a').close()
    sync_data = toml.load(sync_path)

    paks_to_update = {}
    def update_strings(wads, paks_to_update, data, meta):
        if isinstance(meta, String):
            wad = wads[meta.wad_name]

            pak_key = (meta.wad_name, meta.path)
            if pak_key not in paks_to_update:
                paks_to_update[pak_key] = wad.read_pak(meta.path)
            paks_to_update[pak_key].set(meta.indices, data)
        elif isinstance(meta, Strings):
            # convert the dict to a list and proceed as before (this will only work
            # if the format matches)
            data_l = [None] * len(data)
            for k, v in data.items():
                assert int(k) not in data_l
                data_l[int(k)] = v

            wad = wads[meta.wad_name]

            pak_key = (meta.wad_name, meta.path)
            if pak_key not in paks_to_update:
                paks_to_update[pak_key] = wad.read_pak(meta.path)
            paks_to_update[pak_key].set(meta.indices, data_l)
        elif isinstance(data, list):
            for i in range(len(data)):
                update_strings(wads, paks_to_update, data[i], meta[i])
        elif isinstance(data, dict):
            for k in data.keys():
                update_strings(wads, paks_to_update, data[k], meta[k])
        else:
            raise ValueError

    for fname, meta in files.items():
        if not fname.startswith(prefix): continue

        fpath = os.path.join(indir, fname)
        mtime = os.path.getmtime(fpath)
        # only consider edited files
        if fname in sync_data and mtime <= sync_data[fname]: continue

        print('repacking {}'.format(fpath))

        if fname.endswith('.toml'):
            data = toml.load(fpath)
            update_strings(wads, paks_to_update, data, meta)
        else:
            file = open(fpath, 'rb')
            data = meta.repack(wads, file)

            if meta.indices == []:
                wads[meta.wad_name].quick_repack_file(meta.path, data)
            else:
                wad = wads[meta.wad_name]

                pak_key = (meta.wad_name, meta.path)
                if pak_key not in paks_to_update:
                    paks_to_update[pak_key] = wad.read_pak(meta.path)
                paks_to_update[pak_key].set(meta.indices, data)

        sync_data[fname] = mtime

    # repack paks
    for (wad, path), pak in paks_to_update.items():
        wads[wad].quick_repack_file(path, pak.repack())

    # update sync file
    print('writing sync file')
    sync_file = open(sync_path, 'w')
    toml.dump(sync_data, sync_file)
    sync_file.close()

import metadata.report_card
import metadata.presents
import metadata.truth_bullets
import metadata.backgrounds
import metadata.sprites
import metadata.character_names
import metadata.title_screen
import metadata.maps

files = {
        'report_card.toml': report_card.report_card,
        'presents.toml': presents.presents,
        'truth_bullets.toml': truth_bullets.truth_bullets,
        'character_names.toml': character_names.character_names,
        'maps.toml': maps.maps,
}

report_card.add_files(files)
presents.add_files(files)
backgrounds.add_files(files)
sprites.add_files(files)
character_names.add_files(files)
title_screen.add_files(files)
