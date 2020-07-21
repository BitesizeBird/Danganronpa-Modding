import sys
sys.path.append('.')

import formats.wad as wad
import bisect

data = wad.Wad('../../dr2_data.wad')
data_us = wad.Wad('../../dr2_data_us.wad')

data_files = [[0, '<header>']]
for path, file in data.files.items():
    data_files.append([file[0], path])
data_files.sort()
data_offsets = [offset for [offset, _] in data_files]

data_us_files = [[0, '<header>']]
for path, file in data_us.files.items():
    data_us_files.append([file[0], path])
data_us_files.sort()
data_us_offsets = [offset for [offset, _] in data_us_files]

fds = {}
offsets = {}

class WadOpen(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fopen', type=gdb.BP_BREAKPOINT)

    def stop(self):
        path = gdb.parse_and_eval('(char*)$rdi').string()

        WadFinishOpen(path)
        return False

class WadFinishOpen(gdb.FinishBreakpoint):
    def __init__(self, path):
        super().__init__(internal=True)
        self.path = path

    def stop(self):
        try:
            fd = int(gdb.parse_and_eval('((FILE*)$rax)->_fileno'))

            fds[fd] = self.path
            offsets[fd] = 0
        except: # fuck the police
            pass
        return False

class WadClose(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fclose', type=gdb.BP_BREAKPOINT)

    def stop(self):
        fd = int(gdb.parse_and_eval('((FILE*)$rdi)->_fileno'))

        if fd in fds:
            del fds[fd]
            del offsets[fd]

        return False

class WadSeek(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fseeko64', type=gdb.BP_BREAKPOINT)

    def stop(self):
        fd = int(gdb.parse_and_eval('((FILE*)$rdi)->_fileno'))
        offset = gdb.parse_and_eval('(unsigned long long)$rsi')
        whence = gdb.parse_and_eval('(int)$rdx')
        if whence == 0:
            offsets[fd] = offset
        elif whence == 1 and fd in offsets:
            offsets[fd] += offset

        return False

class WadRead(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fread', type=gdb.BP_BREAKPOINT)

    def stop(self):
        ptr = gdb.parse_and_eval('(void*)$rdi')
        size = gdb.parse_and_eval('(size_t)$rsi')
        count = gdb.parse_and_eval('(size_t)$rdx')
        fd = int(gdb.parse_and_eval('((FILE*)$rcx)->_fileno'))

        bytes_ = size*count

        if fd in fds:
            offset = offsets[fd]
            offsets[fd] += bytes_

            if fds[fd] == 'dr2_data.wad':
                idx = bisect.bisect_right(data_offsets, offset)-1
                file = data_files[idx]

                if 'bgm' in file[1] and file[1].endswith('.ogg'): # ignore music files
                    return False

                print('read {} bytes from dr2_data:{} (offset {}) to ptr {}'.format(bytes_, file[1], offset - file[0], ptr))
            elif fds[fd] == 'dr2_data_us.wad':
                idx = bisect.bisect_right(data_us_offsets, offset)-1
                file = data_us_files[idx]

                print('read {} bytes from dr2_data_us:{} (offset {}) to ptr {}'.format(bytes_, file[1], offset - file[0], ptr))

                if data_us_files[idx][1].endswith('.lin'):
                    print('found a lin! stopping')
                    return True

        return False


WadOpen()
WadClose()
WadSeek()
WadRead()
