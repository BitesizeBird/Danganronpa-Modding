from metadata import Tga

def add_files(files):
    files.update({
        'title_screen/characters/{:02}/{}.png'.format(i, j):
            Tga('dr2_data', 'Dr2/data/all/cg/title/seq_island_chara_{:03}.pak'.format(i), j)
        for i in range(1, 18) for j in range(4)})
