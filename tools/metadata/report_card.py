from metadata import PakString, Tga

report_card = {}
_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

# one entry for each student
for i in range(16):
    key = '{:02}'.format(i)

    report_card[key] = {
            'name':       PakString(_wad, _pak, [16, 0*16+i]),
            'height':     PakString(_wad, _pak, [16, 1*16+i]),
            'weigth':     PakString(_wad, _pak, [16, 2*16+i]),
            'chest':      PakString(_wad, _pak, [16, 3*16+i]),
            'blood_type': PakString(_wad, _pak, [16, 4*16+i]),
            'birthday':   PakString(_wad, _pak, [16, 5*16+i]),
            'likes':      PakString(_wad, _pak, [16, 6*16+i]),
            'dislikes':   PakString(_wad, _pak, [16, 7*16+i]),

            'ultimate': [
                PakString(_wad, _pak, [8, 0*16+i]),
                PakString(_wad, _pak, [8, 1*16+i]),
                PakString(_wad, _pak, [8, 2*16+i]),
            ],
    }

    if i > 0:
        report_card[key]['fte_summaries'] = [PakString(_wad, _pak, [9, 5*(i-1)+j]) for j in range(5)]

def add_files(files):
    files.update({
        'report_card/pictures/{:02}.png'.format(i):
            Tga('dr2_data', 'Dr2/data/all/cg/report/tsushimbo_chara_{:03}.tga'.format(i))
        for i in range(19)})
