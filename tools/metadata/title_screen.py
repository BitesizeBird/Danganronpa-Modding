from metadata import Tga

def add_files(files):
    #files['title_screen/island_background.png'] = Tga('dr2_data_us', 'Dr2/data/us/bin/bin_title_l.pak', [1, 2]) #[1,2] or [1,3]?
    #files['title_screen/copyright.png'] = Tga('dr2_data_us', 'Dr2/data/us/bin/bin_title_l.pak', [1, 4]) <- TODO: not indexed
    files['title_screen/game_title.png'] = Tga('dr2_data_us', 'Dr2/data/us/bin/bin_title_l.pak', [1, 5])

    files.update({
        'title_screen/characters/00/{}.png'.format(j):
            Tga('dr2_data_us', 'Dr2/data/us/bin/bin_title_l.pak', [3, j+1])
        for j in range(4)})

    files.update({
        'title_screen/characters/{:02}/{}.png'.format(i, j):
            Tga('dr2_data', 'Dr2/data/all/cg/title/seq_island_chara_{:03}.pak'.format(i), [j])
        for i in range(1, 18) for j in range(4)})
