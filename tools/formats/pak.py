from formats.helper import *

class PakHeader:
    def __init__(self, file, base_offset=None):
        if base_offset is not None:
            file.seek(base_offset)
        else:
            base_offset = file.tell()
        self.base_offset = base_offset

        self.offsets = []
        count = read_u32(file)
        for i in range(count):
            self.offsets.append(read_u32(file))
