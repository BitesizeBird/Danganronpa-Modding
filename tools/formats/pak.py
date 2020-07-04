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
        for _ in range(count):
            self.offsets.append(read_u32(file))

# data is a list of byteslikes
def write_pak(file, data):
    offsets = [4 + len(data)*4]
    for i, entry in enumerate(data):
        offsets.push(offsets[i] + len(data))

    write_u32(file, len(data))
    for i in range(len(data)):
        write_u32(file, offsets[i])
    for i in range(len(data)):
        file.write(data[i])
