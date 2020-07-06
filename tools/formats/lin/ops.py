opcodes = {}

# .lin script operation
class Op:
    def __init__(self, code, name):
        self.code = code
        self.name = name

        opcodes[code] = self

Op(0x06, 'Animation')
Op(0x25, 'Change UI')
Op(0x27, 'Check Character')
Op(0x35, 'Check Flag A')
Op(0x29, 'Check Object')
Op(0x2b, 'Choice')
Op(0x3c, 'End Flag Check')
Op(0x04, 'Filter')
Op(0x03, 'Format')
Op(0x34, 'Go To Label')
Op(0x05, 'Movie')
Op(0x22, 'Fade')
Op(0x1f, 'Flash')
Op(0x26, 'Set Flag')
Op(0x2a, 'Set Label')
Op(0x10, 'Set Report Info')
Op(0x0f, 'Set Title')
Op(0x30, 'Show Background')
Op(0x0a, 'SFX A')
Op(0x0b, 'SFX B')
Op(0x21, 'Speaker')
Op(0x1e, 'Sprite')
Op(0x1a, 'Stop Script')
Op(0x00, 'Text Count')
Op(0x02, 'Text')
Op(0x0c, 'Truth Bullet')
Op(0x08, 'Voice Line')
Op(0x4b, 'Wait For Input')
Op(0x4c, 'Wait Frame')
Op(0x15, 'Load Map')
Op(0x19, 'Load Script')
Op(0x1b, 'Run Script')
Op(0x14, 'Trial Camera')
