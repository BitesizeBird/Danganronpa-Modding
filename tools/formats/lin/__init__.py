NO_TEXT = 1
WITH_TEXT = 2

import argparse

parser = argparse.ArgumentParser(description='.lin disassembler')
parser.add_argument('input')
args = vars(parser.parse_args())

import struct
from ..helper import *

with open(args['input'], 'rb') as inp:
    data = inp.read()
    offset = 0

    # READ HEADER
    lin_type, offset = read_u32(data, offset)
    assert lin_type in [NO_TEXT, WITH_TEXT]
    script_data_offset, offset = read_u32(data, offset)

    if lin_type == WITH_TEXT:
        text_data_offset, offset = read_u32(data, offset)
    else:
        text_data_offset = len(data)
    file_size, offset = read_u32(data, offset)

    # READ SCRIPT DATA
    offset = script_data_offset
    byte, offset = read_u8(data, offset)
    assert byte == 0x70 # opcode marker
    while offset < text_data_offset:
        opcode, offset = read_u8(data, offset)

        parameters_begin = offset
        while offset < text_data_offset:
            if data[offset] == 0x70: break
            offset += 1
        parameters_end = offset

        parameters = data[parameters_begin:parameters_end]

        # map opcodes to names
        if opcode == 0x06:
            opname = 'Animation'
        elif opcode == 0x25:
            opname = 'Change UI'
        elif opcode == 0x27:
            opname = 'Check Character'
        elif opcode == 0x35:
            opname = 'Check Flag A'
        elif opcode == 0x29:
            opname = 'Check Object'
        elif opcode == 0x2b:
            opname = 'Choice'
        elif opcode == 0x3c:
            opname = 'End Flag Check'
        elif opcode == 0x04:
            opname = 'Filter'
        elif opcode == 0x03:
            opname = 'Format'
        elif opcode == 0x34:
            opname = 'Go To Label'
        elif opcode == 0x05:
            opname = 'Movie'
        elif opcode == 0x22:
            opname = 'Fade'
        elif opcode == 0x1f:
            opname = 'Flash'
        elif opcode == 0x26:
            opname = 'Set Flag'
        elif opcode == 0x2a:
            opname = 'Set Label'
        elif opcode == 0x10:
            opname = 'Set Report Info'
        elif opcode == 0x0f:
            opname = 'Set Title'
        elif opcode == 0x30:
            opname = 'Show Background'
        elif opcode == 0x0a:
            opname = 'SFX A'
        elif opcode == 0x0b:
            opname = 'SFX B'
        elif opcode == 0x21:
            opname = 'Speaker'
        elif opcode == 0x1e:
            opname = 'Sprite'
        elif opcode == 0x1a:
            opname = 'Stop Script'
        elif opcode == 0x00:
            opname = 'Text Count'
        elif opcode == 0x02:
            opname = 'Text'
        elif opcode == 0x0c:
            opname = 'Truth Bullet'
        elif opcode == 0x08:
            opname = 'Voice Line'
        elif opcode == 0x4b:
            opname = 'Wait For Input'
        elif opcode == 0x4c:
            opname = 'Wait Frame'
        elif opcode == 0x15:
            opname = 'Load Map'
        elif opcode == 0x19:
            opname = 'Load Script'
        elif opcode == 0x1b:
            opname = 'Run Script'
        elif  opcode == 0x14:
            opname = 'Trial Camera'
        else:
            opname = '?'

        print('{} [{:02x}] - {}'.format(opname, opcode, parameters.hex()))
        offset += 1 # skip the 0x70 byte

    # READ TEXT DATA
    # (pak format)
    offset = text_data_offset
    if lin_type == WITH_TEXT:
        count, offset = read_u32(data, offset)

        for i in range(count):
            pointer, offset = read_u32(data, offset)
            text_begin = text_data_offset + pointer
            text_end = text_begin
            while text_end < len(data):
                word, text_end = read_u16(data, text_end)
                if word == 0:
                    text_end -= 2
                    break

            text_slice = data[text_begin:text_end]
            text_decoded = text_slice.decode('utf-16-le')
            print(text_decoded)
