import json
import bisect
import sys
import re

data_offsets = json.load(open('dr2_data.offsets', 'r'))
data_offsets.sort()
data_o = [offset[0] for offset in data_offsets]

data_us_offsets = json.load(open('dr2_data_us.offsets', 'r'))
data_us_offsets.sort()
data_us_o = [offset[0] for offset in data_us_offsets]


DATA_FD = 41
DATA_US_FD = 42

data_offset = None
data_us_offset = None

seek_re = re.compile('''lseek\(0x([0-9a-f]+), 0x([0-9a-f]+), 0\)\s*= 0x([0-9a-f]+)''')
read_re = re.compile('''read\(0x([0-9a-f]+), 0x([0-9a-f]+), 0x([0-9a-f]+)\)\s*= 0x([0-9a-f]+)''')

for line in sys.stdin:
    seek_match = re.search(seek_re, line)
    read_match = re.search(read_re, line)
    if seek_match is not None:
        fd = int(seek_match.group(1), 16)
        offset = int(seek_match.group(3), 16)

        if fd == DATA_FD: data_offset = offset
        if fd == DATA_US_FD: data_us_offset = offset
    elif read_match is not None:
        fd = int(read_match.group(1), 16)
        pointer = int(read_match.group(2), 16)
        size = int(read_match.group(4), 16)

        if fd == DATA_FD and data_offset is not None:
            idx = bisect.bisect_right(data_o, data_offset)-1

            print('read {} bytes from dr2_data:{} (offset {})'.format(size, data_offsets[idx][1], data_offset - data_offsets[idx][0]))
            data_offset += size
        if fd == DATA_US_FD and data_us_offset is not None:
            idx = bisect.bisect_right(data_us_o, data_us_offset)-1

            print('read {} bytes from dr2_data_us:{} (offset {})'.format(size, data_us_offsets[idx][1], data_us_offset - data_us_offsets[idx][0]))
            data_us_offset += size
    else:
        print('N/A')
