from metadata import PakString

truth_bullets = {}
_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

for i in range(200):
    key = '{:03}'.format(i)

    truth_bullets[key] = {
            'name': PakString(_wad, _pak, [4, i]),
            'descriptions': [
                PakString(_wad, _pak, [5, i]),
                PakString(_wad, _pak, [6, i]),
                PakString(_wad, _pak, [7, i]),
            ],
    }
