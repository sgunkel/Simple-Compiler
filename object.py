#
# Seth Gunkel
#

from enum import Enum, auto

class Type(Enum):
    NIL      = auto()
    NUM      = auto()
    BOOL     = auto()
    STRING   = auto()
    BINARY   = auto() # maybe get rid if this..?
    FUNCTION = auto()

typeName = {
    Type.NIL    : "object",
    Type.NUM    : "number",
    Type.BOOL   : "bool",
    Type.STRING : "string",
}

class object:
    def __init__(self, _type, data):
        self.type = _type
        self.data = data

def TypeOf(obj):
    return typeName[obj.type]



