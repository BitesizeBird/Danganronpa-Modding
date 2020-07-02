import struct

def read_string(file):
    data = bytearray()
    in_ = file.read(2)
    assert in_ == b'\xff\xfe' # byte order mark
    in_ = file.read(2)
    while in_ != b'\0\0':
        data.extend(in_)
        in_ = file.read(2)
    return data.decode('utf-16-le')

def read_u64(data, offset):
    return struct.unpack('<Q', data[offset:offset+8])[0], offset+8
def read_u64(file):
    return struct.unpack('<Q', file.read(8))[0]

def read_u32(data, offset):
    return struct.unpack('<I', data[offset:offset+4])[0], offset+4
def read_u32(file):
    return struct.unpack('<I', file.read(4))[0]

def read_u16(data, offset):
    return struct.unpack('<H', data[offset:offset+2])[0], offset+2
def read_u16(file):
    return struct.unpack('<H', file.read(2))[0]

def read_u8(data, offset):
    return data[offset], offset+1
def read_u8(file):
    return file.read(1)[0]


def write_u64(file, value):
    file.write(struct.pack('<Q', value))
