from metadata import PakString

_wad = 'dr2_data_us'
_pak = 'Dr2/data/us/bin/bin_progress_font_l.pak'

dialogue_speakers = {'{:02}'.format(i): PakString(_wad, _pak, [18, i]) for i in range(64)}
