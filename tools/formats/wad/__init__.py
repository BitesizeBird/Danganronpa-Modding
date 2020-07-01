from ..helper import *

class Wad:
    def __init__(self, file, offset=None):
        if offset is not None:
            file.seek(offset)
        else:
            offset = file.tell()

        # magic bytes
        assert file.read(4) == b'AGAR'
        self.version = [read_u32(file), read_u32(file)]
        header_size = read_u32(file)

        # read file metadata
        self.file_names = []
        self.file_sizes = []
        self.file_offsets = []
        file_count = read_u32(file)
        for i in range(file_count):
            file_name_length = read_u32(file)
            self.file_names.append(file.read(file_name_length).decode())
            self.file_sizes.append(read_u64(file))
            self.file_offsets.append(read_u64(file))

        # read directory metadata
        self.dir_names = []
        self.dir_subfiles = []
        dir_count = read_u32(file)
        for i in range(dir_count):
            dir_name_length = read_u32(file)
            self.dir_names.append(file.read(dir_name_length).decode())
            self.dir_subfiles.append([])
            subfile_count = read_u32(file)
            for j in range(subfile_count):
                subfile_name_length = read_u32(file)
                subfile_name = file.read(subfile_name_length).decode()
                is_directory = read_u8(file) != 0
                self.dir_subfiles[i].append((subfile_name, is_directory))
