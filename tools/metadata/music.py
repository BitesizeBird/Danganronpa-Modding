import toml
from metadata import Raw, LoopPoint
from formats.helper import *

COUNT = 102

def add_files(files):
    files['music.toml'] = {
            '{:03}'.format(i):
                {
                    'loop_start': LoopPoint(i, 4),
                    'loop_end': LoopPoint(i, 8)}
            for i in range(COUNT) if i not in [0, 22, 44, 46, 93, 94] + list(range(62, 92)) + list(range(96, COUNT))}

    for i in range(COUNT):
        files['music/{:03}.ogg'.format(i)] = Raw('dr2_data', 'Dr2/data/all/bgm/dr2_bgm_hca.awb.{:05}.ogg'.format(i))
