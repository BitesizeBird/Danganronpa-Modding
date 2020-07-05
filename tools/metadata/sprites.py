from metadata import Tga

bust_counts = [30, 31, 16, 27, 25, 22, 15, 22,
        27, 24, 26, 24, 21, 24, 24, 22,
        24, 42, 19, 10, 2, 20, 19, 0, 5]

full_body_counts = [30, 31, 20, 27, 25, 22, 20, 52,
        27, 25, 26, 24, 21, 24, 24, 22,
        24, 42, 19, 10, 21, 20, 19]
has_99 = [1, 2, 3, 5, 6, 11, 12, 13, 14, 15, 20, 21, 22]

def add_files(files):
    #BUSTS
    files.update({
        'sprites/busts/{:02}/{:02}.png'.format(i, j):
            Tga('dr2_data', 'Dr2/data/all/cg/bustup_{:02}_{:02}.tga'.format(i, j))
        for i in range(len(bust_counts)) for j in range(bust_counts[i])})

    # exception for fuyuhiko: add additional busts (30 to 51)
    files.update({
        'sprites/busts/07/{:02}.png'.format(j):
            Tga('dr2_data', 'Dr2/data/all/cg/bustup_07_{:02}.tga'.format(j))
        for j in range(30, 52)})
    # exception for monokuma (30 to 53)
    files.update({
        'sprites/busts/16/{:02}.png'.format(j):
            Tga('dr2_data', 'Dr2/data/all/cg/bustup_16_{:02}.tga'.format(j))
        for j in range(30, 54)})

    # FULL BODIES
    for i, count in enumerate(full_body_counts):
        for j in range(count):
            files['sprites/full_body/{:02}/{:02}.png'.format(i, j)] = \
                    Tga('dr2_data', 'Dr2/data/all/texture/stand_{:02}_{:02}.tga'.format(i, j))

        # exception for monokuma (30 to 53)
        if i == 16:
            for j in range(30, 54):
                files['sprites/full_body/{:02}/{:02}.png'.format(i, j)] = \
                        Tga('dr2_data', 'Dr2/data/all/texture/stand_{:02}_{:02}.tga'.format(i, j))

    for i in has_99:
        j = 99
        files['sprites/full_body/{:02}/{:02}.png'.format(i, j)] = \
                Tga('dr2_data', 'Dr2/data/all/texture/stand_{:02}_{:02}.tga'.format(i, j))

