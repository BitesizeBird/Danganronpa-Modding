from ..helper import *
import os

class Wad:
    def __init__(self):
        self.files = {}
        self.dirs = {}

    def read(self, path):
        file = open(path, 'rb')

        # magic bytes
        assert file.read(4) == b'AGAR'
        self.version = [read_u32(file), read_u32(file)]
        header_size = read_u32(file)

        # read file metadata
        self.files.clear()
        file_count = read_u32(file)
        for i in range(file_count):
            file_metadata_offset = file.tell()
            file_name_length = read_u32(file)
            file_name = file.read(file_name_length).decode()
            file_size = read_u64(file)
            file_offset = read_u64(file)
            self.files[file_name] = dict(
                metadata_offset = file_metadata_offset,
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

        # IMPORTANT: fix file offsets
        base_offset = file.tell()
        for _, file_ in self.files.items():
            file_['offset'] += base_offset

        file.close()

    def update_file(self, path, name, data):
        assert name in self.files

        old_size = self.files[name]['size']
        new_size = len(data)
        self.files[name]['size'] = new_size

        file = open(path, 'rb+')
        file.seek(self.files[name]['metadata_offset'])
        file_name_length = read_u32(file)
        file_name = file.read(file_name_length).decode()
        assert file_name == name
        # write new size
        write_u64(file, new_size)

        if new_size <= old_size:
            # don't write new offset
            file.seek(self.files[name]['offset'])
            file.write(data)
        else:
            # write new offset (file end)
            old_file_size = os.path.getsize(path)
            write_u64(file, old_file_size)
            # reallocate
            file.close()
            file = open(path, 'a')
            file.write(data)
        file.close()

    def read_file(self, path, name):
        assert name in self.files

        file = open(path, 'rb')
        file.seek(self.files[name]['offset'])
        buffer = file.read(self.files[name]['size'])
        file.close()
        return buffer
