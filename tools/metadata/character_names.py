from metadata import String, Tga

_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

character_names = {'{:02}'.format(i): String(_wad, _pak, [18, i]) for i in range(64)}

def add_files(files):
    for i in range(32):
        files['character_names/{:02}.png'.format(i)] = Tga('dr2_data_us', 'Dr2/data/us/cg/chara_name.pak', [i])
