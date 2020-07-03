from metadata import DataPath

items = {}
_wad = 'dr2_data_us.wad'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

# one entry for each item
for i in range(140):
    key = '{:03}'.format(i)

    items[key] = {
            'name':        DataPath(_wad, _pak, [2, i]),
            'description': DataPath(_wad, _pak, [3, i]),
    }
