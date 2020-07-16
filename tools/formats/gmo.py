import struct
import io

def read_chunk_header(data):
    return struct.unpack_from('<HHI', data)

class Gmo:
    def __init__(self, data):
        # check magic numbers
        assert data[0:16] == b'OMG.00.1PSP\00\00\00\00\00'
        # skip over top level entry (0x0002)
        data = data[16:]
        chunk_type, header_size, chunk_size = read_chunk_header(data)
        assert chunk_type == 0x0002
        data = data[header_size:]

        self.subfiles = []

        # read subfiles
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)
            assert chunk_type == 3

            self.subfiles.append(GmoSubfile(data[8:header_size], data[header_size:chunk_size]))

            data = data[chunk_size:]

class GmoSubfile:
    def __init__(self, header, data):
        self.objects = []
        self.materials = []
        self.textures = []

        # read chunks
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)

            if chunk_type == 5: # object
                self.objects.append(GmoObject(data[8:header_size], data[header_size:chunk_size]))
            elif chunk_type == 8: # material
                self.materials.append(GmoMaterial(data[8:header_size], data[header_size: chunk_size]))
            elif chunk_type == 0xa: # texture
                self.read_texture(data[8:header_size], data[header_size:chunk_size])
            else:
                print('# TODO: subfile chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

    def read_texture(self, header, data):
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)
            assert chunk_type == 0x8012 and header_size == 0

            if chunk_type == 0x8012: # texture... path?? in development???
                # oh my god its even a png
                # maybe theres a toggle to use this instead of the usual tga?
                path = data[8:chunk_size].decode().rstrip('\00')
                self.textures.append(path)
            else:
                print('# TODO: texture chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

    def write_mtl(self, mtl):
        for i, material in enumerate(self.materials):
            print('newmtl {}'.format(i), file=mtl)
            print('map_Kd {}', self.textures[material.texture_index], file=mtl)
            print(file=mtl)

class GmoVertex:
    def __init__(self, uv, norm, pos):
        self.uv = uv
        self.norm = norm
        self.pos = pos

class GmoMesh:
    def __init__(self, material_index, faces):
        self.material_index = material_index
        self.faces = faces

class GmoObject:
    def __init__(self, header, data):
        self.meshes = []
        self.vertices = []

        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)

            if chunk_type == 6: # mesh
                self.meshes.append(GmoMesh(data[8:header_size], data[header_size:chunk_size]))
            elif chunk_type == 7: # vertex arr)y
                _, _, vertex_count = struct.unpack_from('<HHI', data[header_size:])
                vertex_size = (chunk_size-header_size) // vertex_count

                vertex_data_offset = chunk_size - vertex_count*vertex_size

                for i in range(vertex_count):
                    u, v, nx, ny, nz, x, y, z = struct.unpack_from('<ff fff fff', data[vertex_data_offset + i*vertex_size:])

                    self.vertices.append(GmoVertex((u, v), (nx, ny, nz), (x, y, z)))
            else:
                print('# TODO: model surface chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

    def write_obj(self, obj, mtl_path):
        print('mtllib {}'.format(mtl_path), file=obj)
        print(file=obj)

        for vertex in self.vertices:
            print('v {} {} {}'.format(*vertex.pos), file=obj)
            print('vt {} {}'.format(vertex.uv[0], 1.0 - vertex.uv[1]), file=obj)
            print('vn {} {} {}'.format(*vertex.norm), file = obj)
        print(file=obj)

        for i, mesh in enumerate(self.meshes):
            print('g {}'.format(i), file=obj)
            print('usemtl {}'.format(mesh.material_index), file=obj)
            for face in mesh.faces:
                print('f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c} {d}/{d}/{d}'.format(a=face[0]+1, b=face[1]+1, c=face[2]+1, d=face[3]+1), file=obj)

class GmoMesh:
    def __init__(self, header, data):
        self.faces = []

        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)
            
            if chunk_type == 0x8061: # material info
                self.material_index = struct.unpack_from('< H', data[8:])[0] - 0x2000
            elif chunk_type == 0x8066: # index data
                assert header_size == 0
                header_size = 8

                _, _, primitive_type = struct.unpack_from('< HHI', data[header_size:])

                if primitive_type == 3: # triangles
                    print('# TODO: triangle primitives')
                    raise 'bitch fix this'
                elif primitive_type == 4: # quads
                    stripe_size, stripe_count = struct.unpack_from('< II', data[header_size+8:])

                    for i in range(stripe_count):
                        for j in range(stripe_size//2 - 1):
                            a, b, d, c = struct.unpack_from('< HHHH', data[header_size+16 + i*stripe_size*2 + j*4:])

                            self.faces.append((a, b, c, d))
                else:
                    print('# WARN: unknown primitive type {}'.format(primitive_type))
            else:
                print('# TODO: mesh chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]

class GmoMaterial:
    def __init__(self, header, data):
        while len(data) > 0:
            chunk_type, header_size, chunk_size = read_chunk_header(data)

            if chunk_type == 9: # texture reference
                self.texture_index = struct.unpack_from('<H', data[header_size+8:])[0] - 0x2000
            else:
                print('# TODO: material chunk type {:04x}'.format(chunk_type))

            data = data[chunk_size:]
