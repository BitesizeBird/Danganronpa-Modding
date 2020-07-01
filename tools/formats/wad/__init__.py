from ..helper import *

class Wad:
    def __init__(self):
        self.files = {}
        self.dirs = {}

    def read(self, file, offset=None):
        if offset is not None:
            file.seek(offset)
        else:
            offset = file.tell()

        # magic bytes
        assert file.read(4) == b'AGAR'
        self.version = [read_u32(file), read_u32(file)]
        header_size = read_u32(file)

        # read file metadata
        self.files.clear()
        file_count = read_u32(file)
        for i in range(file_count):
            file_name_length = read_u32(file)
            file_name = file.read(file_name_length).decode()
            file_size = read_u64(file)
            file_offset = offset + read_u64(file)
            self.files[file_name] = dict(
                size = file_size,
                offset = file_offset)

        # read directory metadata
        self.dirs.clear()
        dir_count = read_u32(file)
        for i in range(dir_count):
            dir_name_length = read_u32(file)
            dir_name = file.read(dir_name_length).decode()
            dir_subfiles = {}
            subfile_count = read_u32(file)
            for j in range(subfile_count):
                subfile_name_length = read_u32(file)
                subfile_name = file.read(subfile_name_length).decode()
                is_directory = read_u8(file) != 0
                dir_subfiles[subfile_name] = dict(
                    name = subfile_name,
                    is_directory = is_directory)
            self.dirs[dir_name] = dict(
                subfiles = dir_subfiles)
