from formats.helper import *
import formats.lin.ops
import formats.pak as pak
import struct

NO_TEXT = 1
WITH_TEXT = 2

class LinScript:
    def read_from(wad, path):
        self = LinScript()

        entry = wad.files[path]
        wad.file.seek(entry[0])

        lin_type = read_u32(wad.file)
        assert lin_type in [NO_TEXT, WITH_TEXT]
        script_data_offset = read_u32(wad.file)
        if lin_type == WITH_TEXT:
            text_data_offset = read_u32(wad.file)
        else:
            text_data_offset = entry[1]

        # READ SCRIPT DATA
        self.script = []
        wad.file.seek(entry[0] + script_data_offset)
        while wad.file.tell() < entry[0] + text_data_offset:
            if wad.file.peek(2).startswith(b'\00\00'): break
            op = ops.read_op(wad.file)
            if op is None: break
            self.script.append(op)

        # READ TEXT DATA
        if lin_type == WITH_TEXT:
            self.strings = pak.Pak(wad.file, entry[0] + text_data_offset, entry[1] - text_data_offset).strings()
            import pprint
            pprint.pprint(self.strings)

        for op in self.script:
            if isinstance(op, ops.Text):
                print('{} [{:02x}] {}'.format(op.name, op.code, repr(self.strings[op.index])))
            else:
                print(op)

        return self
