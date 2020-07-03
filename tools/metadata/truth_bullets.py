from metadata import DataPath

truth_bullets = {}
_wad = 'dr2_data_us.wad'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

for i in range(200):
    key = '{:03}'.format(i)

    truth_bullets[key] = {
            'name': DataPath(_wad, _pak, [4, i]),
            'descriptions': [
                DataPath(_wad, _pak, [5, i]),
                DataPath(_wad, _pak, [6, i]),
                DataPath(_wad, _pak, [7, i]),
            ],
    }
