from metadata import PakString

presents = {}
_wad = 'dr2_data_us.wad'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

# one entry for each present
for i in range(140):
    key = '{:03}'.format(i)

    presents[key] = {
            'name':        PakString(_wad, _pak, [2, i]),
            'description': PakString(_wad, _pak, [3, i]),
    }
