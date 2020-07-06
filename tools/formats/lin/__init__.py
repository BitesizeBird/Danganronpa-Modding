from formats.helper import *
import formats.lin.ops
import formats.pak as pak

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
        wad.file.seek(entry[0] + script_data_offset)
        assert read_u8(wad.file) == 0x70 # opcode marker
        while wad.file.tell() < entry[0] + text_data_offset:
            opcode = read_u8(wad.file)
            parameters = bytearray()

            byte = read_u8(wad.file)
            while byte != 0x70:
                parameters.append(byte)
                byte = read_u8(wad.file)

            op = ops.opcodes.get(opcode)

            print(op.name if op is not None else '?', parameters.hex())

        # READ TEXT DATA
        if lin_type == WITH_TEXT:
            self.strings = pak.Pak(wad.file, entry[0] + text_data_offset, entry[1] - text_data_offset).strings()

        return self
