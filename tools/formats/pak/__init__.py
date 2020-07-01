from ..helper import *

class Pak:
    def __init__(self, file, offset=None):
        if offset is not None:
            file.seek(offset)
        else:
            offset = file.tell()

        self.offsets = []
        count = read_u32(file)
        for i in range(count):
            self.offsets.append(read_u32(file) + offset)
