from formats.gmo import Gmo
import sys
import os

Gmo(open(sys.argv[1], 'rb').read())
