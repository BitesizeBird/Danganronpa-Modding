import sys
sys.path.append('.')

import formats.wad as wad
import bisect
import os

class Wad:
    def __init__(self, path):
        self.wad = wad.Wad(path)
        #self.path = path

        self.files = [[0, '<header>']]
        for path, file in self.wad.files.items():
            self.files.append([file[0], path])
        self.files.sort()
        self.offsets = [offset for [offset, _] in self.files]

wads = {}
fileptrs = {}
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
            fileptr = int(gdb.parse_and_eval('(FILE*)$rax'))

            fileptrs[fileptr] = self.path
            offsets[fileptr] = 0
        except: # fuck the police
            pass
        return False

class WadClose(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fclose', type=gdb.BP_BREAKPOINT)

    def stop(self):
        fileptr = int(gdb.parse_and_eval('(FILE*)$rdi'))

        if fileptr in fileptrs:
            del fileptrs[fileptr]
            del offsets[fileptr]

        return False

class WadSeek(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fseeko64', type=gdb.BP_BREAKPOINT)

    def stop(self):
        fileptr = int(gdb.parse_and_eval('(FILE*)$rdi'))
        offset = gdb.parse_and_eval('(unsigned long long)$rsi')
        whence = gdb.parse_and_eval('(int)$rdx')
        if whence == 0:
            offsets[fileptr] = offset
        elif whence == 1 and fileptr in offsets:
            offsets[fileptr] += offset

        return False

class WadRead(gdb.Breakpoint):
    def __init__(self):
        super().__init__('fread', type=gdb.BP_BREAKPOINT)

    def stop(self):
        global show_reads
        global break_on

        ptr = gdb.parse_and_eval('(void*)$rdi')
        size = gdb.parse_and_eval('(size_t)$rsi')
        count = gdb.parse_and_eval('(size_t)$rdx')
        fileptr = int(gdb.parse_and_eval('(FILE*)$rcx'))

        bytes_ = size*count

        if fileptr in fileptrs:
            offset = offsets[fileptr]
            offsets[fileptr] += bytes_

            name = fileptrs[fileptr]
            if name in wads:
                wad = wads[name]
                idx = bisect.bisect_right(wad.offsets, offset)-1
                file = wad.files[idx]
                wad_offset = file[0]
                wad_path = file[1]

                if show_reads:
                    print('reading {} bytes from dr2_data:{} (offset {}) to ptr {}'.format(bytes_, wad_path, offset - wad_offset, ptr))

                for ext in break_on:
                    if wad_path.endswith(ext):
                        break_on.remove(ext)
                        print('BREAK: reading {} bytes from dr2_data:{} (offset {}) to ptr {}'.format(bytes_, wad_path, offset - wad_offset, ptr))
                        return True

        return False

WadOpen()
WadClose()
WadSeek()
WadRead()

def register_wad(path):
    name = os.path.basename(path)
    wads[name] = Wad(path)
def register_all(path):
    wads["dr2_data.wad"] = Wad(os.path.join(path, "dr2_data.wad"))
    wads["dr2_data_us.wad"] = Wad(os.path.join(path, "dr2_data_us.wad"))
    wads["dr2_data_keyboard.wad"] = Wad(os.path.join(path, "dr2_data_keyboard.wad"))
    wads["dr2_data_keyboard_us.wad"] = Wad(os.path.join(path, "dr2_data_keyboard_us.wad"))

show_reads = False
break_on = set()
