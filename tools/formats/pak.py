from formats.helper import *
import io


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

    def extract_list(self, file, size):
        result = []
        for i, offset in enumerate(self.offsets):
            begin = self.base_offset + offset
            end = self.base_offset + (self.offsets[i+1] if i < len(self.offsets)-1 else size)
            file.seek(begin)
            result.append(file.read(end - begin))
        return result

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

class Pak:
    def __init__(self, file, base_offset, size):
        self.header = PakHeader(file, base_offset)
        offsets = self.header.offsets + [size]

        self.entries = []
        for i, offset in enumerate(self.header.offsets):
            file.seek(base_offset + offset)
            self.entries.append(file.read(offsets[i+1] - offset))

    def get(self, indices):
        if len(indices) == 0: return self

        entry = self.entries[indices[0]]
        if len(indices) == 1: return entry

        if not isinstance(entry, Pak):
            entry = Pak(io.BytesIO(entry), 0, len(entry))
            self.entries[indices[0]] = entry
        return entry.get(indices[1:])

    def set(self, indices, value):
        if len(indices) == 0: raise ValueError

        if len(indices) == 1:
            self.entries[indices[0]] = value
        else:
            entry = self.entries[indices[0]]
            if not isinstance(entry, Pak):
                entry = Pak(io.BytesIO(entry), 0, len(entry))
                self.entries[indices[0]] = entry
            entry.set(indices[1:], value)

    def repack(self):
        entries = []
        for entry in self.entries:
            if isinstance(entry, Pak):
                entries.append(entry.repack())
            elif isinstance(entry, str):
                entries.append(b'\xff\xfe' + entry.encode('utf-16-le') + b'\x00\x00')
            else:
                entries.append(entry)

        offsets = [4 + 4*len(self.entries)]
        for i, entry in enumerate(entries):
            offsets.append(offsets[i] + len(entry))

        f = io.BytesIO()
        write_u32(f, len(entries))
        for i in range(len(entries)):
            write_u32(f, offsets[i])
        for entry in entries:
            f.write(entry)

        return f.getbuffer()
