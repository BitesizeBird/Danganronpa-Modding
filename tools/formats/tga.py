from .helper import *

# returns (RGBA8 data, width, height)
def read_tga(file, offset=None):
    if offset is not None:
        file.seek(offset)
    else:
        offset = file.tell()

    # read header
    idfield_length = read_u8(file)
    color_map_type = read_u8(file)
    assert color_map_type == 1
    image_type = read_u8(file)
    assert color_map_type == 1

    color_map_offset = read_u16(file)
    color_map_length = read_u16(file)
    color_map_entry_size = read_u8(file)
    assert color_map_entry_size in [24, 32]

    x_origin = read_u16(file)
    y_origin = read_u16(file)
    width = read_u16(file)
    height = read_u16(file)
    pixel_size = read_u8(file)
    descriptor_byte = read_u8(file)
    assert descriptor_byte == 0

    idfield = file.read(idfield_length)

    # read color data
    color_map = []
    for _ in range(color_map_length):
        if color_map_entry_size == 24:
            color = file.read(3)
            color_map.append((color[2], color[1], color[0]))
        elif color_map_entry_size == 32:
            color = file.read(4)
            color_map.append((color[2], color[1], color[0], color[3]))

    # read image data
    image_data = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(read_u8(file))
        image_data.append(row)
    # fix row ordering
    image_data.reverse()

    return (color_map, image_data, width, height)
