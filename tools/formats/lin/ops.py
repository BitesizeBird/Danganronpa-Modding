from formats.helper import *
import copy

opcodes = {}

def read_op(file):
    byte = read_u8(file)
    if byte != 0x70: # opcode marker
        return None
    opcode = read_u8(file)
    op = copy.copy(opcodes.get(opcode)) or Op(opcode, '???', False)
    op.read_parameters(file)
    return op

# .lin script operation
class Op:
    def __init__(self, code, name, register=True):
        self.code = code
        self.name = name

        if register:
            assert code not in opcodes
            opcodes[code] = self

    def read_parameters(self, file):
        self.parameters = bytearray()
        while file.peek(1)[0] != 0x70:
            self.parameters.append(read_u8(file))

    def __str__(self):
        return '{} [{:02x}] {}'.format(self.name, self.code, self.format_parameters())
    def format_parameters(self):
        return self.parameters.hex()

class NoParams(Op):
    def read_parameters(self, file):
        pass
    def format_parameters(self):
        return ''

class Text(Op):
    def read_parameters(self, file):
        self.index = read_u16_be(file)
    def format_parameters(self):
        return str(self.index)

# both goto and jump
class SwitchScript(Op):
    def read_parameters(self, file):
        self.chapter = read_u8(file)
        self.scene = read_u16_be(file)
        self.room = read_u16_be(file)
    def format_parameters(self):
        return '{} {} {}'.format(self.chapter, self.scene, self.room)

Op(0x00, 'TextCount')
Text(0x02, 'Text')
Op(0x03, 'Format')
Op(0x04, 'Filter')
Op(0x05, 'Movie')
Op(0x06, 'Animation')
Op(0x08, 'Voice Line')
Op(0x09, 'Music')
Op(0x0a, 'SfxA')
Op(0x0b, 'SfxB')
Op(0x0c, 'TruthBullet')
Op(0x0f, 'SetTitle')

Op(0x10, 'SetReportInfo')
Op(0x14, 'TrialCamera')
Op(0x15, 'LoadMap')
SwitchScript(0x19, 'GoToScript')
NoParams(0x1a, 'StopScript')
SwitchScript(0x1b, 'CallScript')
NoParams(0x1c, 'ReturnFromCall')
Op(0x1e, 'Sprite')
Op(0x1f, 'Flash')

Op(0x21, 'Speaker')
Op(0x22, 'Fade')
Op(0x25, 'ChangeUI')
Op(0x26, 'SetFlag')
Op(0x27, 'CheckCharacter')
Op(0x29, 'CheckObject')
Op(0x2a, 'SetLabel')
Op(0x2b, 'Choice')
Op(0x2d, 'CameraFlash')

Op(0x30, 'ShowBackground')
Op(0x32, 'TruthBullets Loaded')
Op(0x34, 'GoToLabel')
Op(0x35, 'CheckFlagA')
Op(0x37, 'ShowCG')
Op(0x3a, 'SetGameState')
Op(0x3b, 'Difficulty')
Op(0x3c, 'EndFlagCheck')

NoParams(0x4b, 'WaitForInput')
NoParams(0x4c, 'WaitFrame')
