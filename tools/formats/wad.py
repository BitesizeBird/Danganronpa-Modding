from formats.helper import *
import os

class WadHeader:
    def __init__(self, file):
        header_begin = file.tell()

        # magic bytes
        assert file.read(4) == b'AGAR'
        self.version = [read_u32(file), read_u32(file)]
        read_u32(file) # ignore this field

        # read file metadata
        self.files = []
        file_count = read_u32(file)
        for i in range(file_count):
            file_metadata_offset = file.tell()
            file_path_length = read_u32(file)
            file_path = file.read(file_path_length).decode()
            file_size = read_u64(file)
            file_offset = read_u64(file)
            self.files.append({
                'path': file_path,
                'size': file_size,
                'offset': file_offset,
                'metadata_offset': file_metadata_offset})

        # read directory metadata
        self.dirs = []
        dir_count = read_u32(file)
        for i in range(dir_count):
            dir_path_length = read_u32(file)
            dir_path = file.read(dir_path_length).decode()
            dir_subfiles = []
            subfile_count = read_u32(file)
            for j in range(subfile_count):
                subfile_name_length = read_u32(file)
                subfile_name = file.read(subfile_name_length).decode()
                is_directory = read_u8(file) != 0
                dir_subfiles.append({
                    'name': subfile_name,
                    'is_directory': is_directory})
            self.dirs.append({
                'path': dir_path,
                'subfiles': dir_subfiles})
        self.header_size = file.tell() - header_begin

class Wad:
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'rb')
        self.header = WadHeader(self.file)

        self.files = {file['path']: (self.header.header_size + file['offset'], file['size'], idx) for idx, file in enumerate(self.header.files)}

    def read_file(self, path):
        self.file.seek(self.files[path][0])
        return self.file.read(self.files[path][1])

    def update_file(self, path, data):
        old_size = self.files[path][1]
        new_size = len(data)
        self.files[path][1] = new_size

        self.file.close()
        file = open(self.path, 'rb+')
        metadata_offset = self.header.files[self.files[path][2]]['metadata_offset']
        file.seek(metadata_offset)
        # read and compare path length
        assert read_u32(file) == len(path)
        # read and compare path
        assert file.read(len(path)).decode() == path
        # write new size
        write_u64(file, new_size)

        if new_size <= old_size:
            # don't write new offset
            file.seek(self.files[path][0])
            file.write(data)
        else:
            # write new offset (file end)
            old_file_size = os.path.getsize(self.path)
            write_u64(file, old_file_size - self.header.header_size)
            # reallocate
            file.close()
            file.open(self.path, 'ab')
            file.write(data)
        file.close()
        
        self.file = open(self.path, 'rb')
