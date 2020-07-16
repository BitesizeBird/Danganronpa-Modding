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
    assert image_type == 1

    color_map_offset = read_u16(file)
    assert color_map_offset == 0
    color_map_length = read_u16(file)
    color_map_entry_size = read_u8(file)
    assert color_map_entry_size in [24, 32]

    x_origin = read_u16(file)
    y_origin = read_u16(file)
    width = read_u16(file)
    height = read_u16(file)
    pixel_size = read_u8(file)
    assert pixel_size == 8
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
    image_data = file.read(width*height)
    image_data = [image_data[width*i:width*(i+1)] for i in range(height)]

    # fix row ordering
    image_data.reverse()

    return color_map, image_data

def write_tga(file, color_map, image_data):
    height = len(image_data)
    width = len(image_data[0])

    # write header
    write_u8(file, 0)
    write_u8(file, 1)
    write_u8(file, 1)
    write_u16(file, 0) # color map offset
    write_u16(file, len(color_map)) # color map size
    assert len(color_map[0]) in [3, 4]
    write_u8(file, 24 if len(color_map[0]) == 3 else 32)

    write_u16(file, 0)
    write_u16(file, 0)
    write_u16(file, width)
    write_u16(file, height)
    write_u8(file, 8)
    assert len(color_map) <= 256
    write_u8(file, 0)

    # write color map
    for color in color_map:
        write_u8(file, color[2])
        write_u8(file, color[1])
        write_u8(file, color[0])
        if len(color) > 3: write_u8(file, color[3])

    # write image data
    for row in reversed(image_data):
        for pixel in row:
            write_u8(file, pixel)
