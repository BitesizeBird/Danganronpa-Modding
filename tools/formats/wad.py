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
                'offset': file_offset})

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

#    def update_file(self, path, name, data):
#        assert name in self.files
#
#        old_size = self.files[name]['size']
#        new_size = len(data)
#        self.files[name]['size'] = new_size
#
#        file = open(path, 'rb+')
#        file.seek(self.files[name]['metadata_offset'])
#        file_name_length = read_u32(file)
#        file_name = file.read(file_name_length).decode()
#        assert file_name == name
#        # write new size
#        write_u64(file, new_size)
#
#        if new_size <= old_size:
#            # don't write new offset
#            file.seek(self.files[name]['offset'])
#            file.write(data)
#        else:
#            # write new offset (file end)
#            old_file_size = os.path.getsize(path)
#            write_u64(file, old_file_size - self._base_offset)
#            # reallocate
#            file.close()
#            file = open(path, 'ab')
#            file.write(data)
#        file.close()
#
#    def read_file(self, path, name):
#        assert name in self.files
#
#        file = open(path, 'rb')
#        file.seek(self.files[name]['offset'])
#        buffer = file.read(self.files[name]['size'])
#        file.close()
#        return buffer
