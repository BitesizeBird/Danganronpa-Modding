from metadata import String

truth_bullets = {}
_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

for i in range(200):
    key = '{:03}'.format(i)

    truth_bullets[key] = {
            'name': String(_wad, _pak, [4, i]),
            'descriptions': [
                String(_wad, _pak, [5, i]),
                String(_wad, _pak, [6, i]),
                String(_wad, _pak, [7, i]),
            ],
    }
