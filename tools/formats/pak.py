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

    # only works when the pak only contains strings nested inside paks
    def extract_strings(self, file):
        result = []
        for offset in self.offsets:
            file.seek(self.base_offset + offset)
            # determine whether it's a string or another pak
            bom = file.read(2)
            if bom == b'\xff\xfe':
                # string
                file.seek(self.base_offset + offset)
                result.append(read_string(file))
                pass
            else:
                # pak
                header = PakHeader(file, self.base_offset + offset)
                result.append(header.extract_strings(file))
                pass
        return(result)

def lists_to_pak(l):
    import io

    if isinstance(l, str):
        return b'\xff\xfe' + l.encode('utf-16-le') + b'\x00\x00'
    elif isinstance(l, list):
        entries = [l_to_pak(e) for e in l]
        offsets = [4 + 4*len(entries)]
        for i, entry in enumerate(entries):
            offsets.append(offsets[i] + len(entry))

        f = io.BytesIO()
        write_u32(f, len(entries))
        for i in range(len(entries)):
            write_u32(f, offsets[i])
        for entry in entries:
            f.write(entry)

        return f.getbuffer()
    else:
        return l

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
