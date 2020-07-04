import sys
import os
import toml
import formats.wad as wad
import formats.pak as pak
from metadata.report_card import report_card as report_card_meta

_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

report_card = toml.load(os.path.join(sys.argv[1], 'report_card.toml'))
dr2_data_us = wad.Wad(sys.argv[2])
bin_progress_font_l = pak.PakHeader(dr2_data_us.file, dr2_data_us.files[_pak][0])
bin_progress_font_l_strings = bin_progress_font_l.extract_strings(dr2_data_us.file)

def replace_strings(strings, data, meta):
    if isinstance(data, str):
        indices = meta.pak_indices
        while len(indices) > 1:
            strings = strings[indices[0]]
            indices.pop(0)
        strings[indices[0]] = data
    elif isinstance(data, list):
        for i in range(len(data)):
            replace_strings(strings, data[i], meta[i])
    elif isinstance(data, dict):
        for k in data.keys():
            replace_strings(strings, data[k], meta[k])
    else:
        raise ValueError

replace_strings(bin_progress_font_l_strings, report_card, report_card_meta)

new_bin_progress_font_l = pak.strings_to_pak(bin_progress_font_l_strings)
dr2_data_us.update_file(_pak, new_bin_progress_font_l)
