from metadata import PakString, Tga

COUNT = 140

presents = {}
_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

# one entry for each present
for i in range(COUNT):
    key = '{:03}'.format(i)

    presents[key] = {
            'name':        PakString(_wad, _pak, [2, i]),
            'description': PakString(_wad, _pak, [3, i]),
    }

def add_files(files):
    files.update({
        'presents/{:03}.png'.format(i): Tga('dr2_data', 'Dr2/data/all/cg/present/present_ico_{:03}.tga'.format(i))
        for i in range(COUNT)})
