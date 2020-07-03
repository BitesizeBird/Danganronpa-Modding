import formats.pak as pak
from formats.helper import read_string

class PakString:
    def __init__(self, wad_name, pak_path, pak_indices):
        self.wad_name = wad_name
        self.pak_path = pak_path
        self.pak_indices = pak_indices

    # assumes the file refers to self.wad_name
    def extract_string(self, wad_header, file):
        offset = wad_header.header_size + next(entry['offset'] for entry in wad_header.files if entry['path'] == self.pak_path)

        for index in self.pak_indices:
            pak_header = pak.PakHeader(file, offset)
            offset = pak_header.base_offset + pak_header.offsets[index]

        file.seek(offset)
        value = read_string(file)
        return value

# assumes there is only dr2_data_us.wad
def extract_from_metadata(wad_header, file, meta):
    if isinstance(meta, PakString):
        return meta.extract_string(wad_header, file)
    elif isinstance(meta, list):
        return [extract_from_metadata(wad_header, file, v) for v in meta]
    elif isinstance(meta, dict):
        return {k: extract_from_metadata(wad_header, file, v) for k, v in meta.items()}
    else:
        raise ValueError

from .report_card import report_card
from .presents import presents
from .truth_bullets import truth_bullets

files = {
        'report_card.toml': report_card,
        'presents.toml': presents,
        'truth_bullets.toml': truth_bullets,
}
