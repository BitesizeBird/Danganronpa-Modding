_codes_to_names = {}
_names_to_codes = {}

def _register_op(code, name):
    _codes_to_names[code] = name
    _names_to_codes[name] = code

_register_op(0x06, 'Animation')
_register_op(0x25, 'Change UI')
_register_op(0x27, 'Check Character')
_register_op(0x35, 'Check Flag A')
# TODO
