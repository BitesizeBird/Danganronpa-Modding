import struct
import io

def read_chunk_header(data):
    return struct.unpack_from('<HHI', data)

class Gmo:
    def __init__(self, data):
        # check magic numbers
        assert data[0:16] == b'OMG.00.1PSP\00\00\00\00\00'
        # skip over top level file (0x0002)
        data = data[16:]
        chunk_type, header_size, chunk_size = read_chunk_header(data)
        assert chunk_type == 0x0002
        data = data[header_size:]

        # read subfiles
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)
            assert chunk_type == 3
            self.read_subfile(data[8:header_size], data[header_size:chunk_size])

            data = data[chunk_size:]

    def read_subfile(self, header, data):
        # read chunks
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)

            if chunk_type == 5: # model surface
                self.read_model_surface(data[8:header_size], data[header_size:chunk_size])
            else:
                print('# TODO: chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

    def read_model_surface(self, header, data):
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)

            if chunk_type == 6: # mesh
                self.read_mesh(data[8:header_size], data[header_size:chunk_size])
            elif chunk_type == 7: # vertex array
                #print(data[header_size:chunk_size].hex())

                _, _, vertex_count = struct.unpack_from('<HHI', data[header_size:])
                vertex_size = (chunk_size-header_size) // vertex_count

                vertex_data_offset = chunk_size - vertex_count*vertex_size

                for i in range(vertex_count):
                    u, v, nx, ny, nz, x, y, z = struct.unpack_from('<ff fff fff', data[vertex_data_offset + i*vertex_size:])

                    print('v {} {} {}'.format(x, y, z))
                    print('vt {} {}'.format(u, 1.0 - v))
                    print('vn {} {} {}'.format(nx, ny, nz))
            else:
                print('# TODO: model surface chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

    def read_mesh(self, header, data):
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)
            
            if chunk_type == 0x8061: # material info
                print('# TODO: mesh material info')
            elif chunk_type == 0x8066: # index data
                assert header_size == 0
                header_size = 8

                _, _, primitive_type = struct.unpack_from('< HHI', data[header_size:])

                if primitive_type == 3: # triangles
                    print('# TODO: triangle primitives')
                elif primitive_type == 4: # quads
                    stripe_size, stripe_count = struct.unpack_from('< II', data[header_size+8:])

                    for i in range(stripe_count):
                        for j in range(stripe_size//2 - 1):
                            a, b, d, c = struct.unpack_from('< HHHH', data[header_size+16 + i*stripe_size*2 + j*4:])
                            print('#[{} {} {} {}]'.format(a, b, c, d))
                            print('f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c} {d}/{d}/{d}'.format(a=a+1, b=b+1, c=c+1, d=d+1))
                else:
                    print('# WARN: unknown primitive type {}'.format(primitive_type))
            else:
                print('# TODO: mesh chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]
