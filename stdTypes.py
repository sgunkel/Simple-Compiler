#
# Seth Gunkel
#

from signatures import *
from object import *
from decimal import Decimal

"""
  Standard methods for the standard types (number, string, etc).
"""

'''
    number operator+(number lhs, number rhs)
    number operator-(number lhs, number rhs)
    number operator*(number lhs, number rhs)
    number operator/(number lhs, number rhs)
    number operator-()
    bool   operator==(number lhs, number rhs)
    bool   operator!=(number lhs, number rhs)
    bool   operator<(number lhs, number rhs)
    bool   operator>(number lhs, number rhs)
    bool   operator<=(number lhs, number rhs)
    bool   operator>=(number lhs, number rhs)
    string ToString()
'''
def stdNumber(callables):
    argList = [ "number", "number" ]
    retType = "number"

    def splitArgs(args):
        return Decimal(args[0].data), Decimal(args[1].data)
    def toObj(func):
        nonlocal retType, argList
        sig = nativeSig(retType, argList, func)
        return object(Type.FUNCTION, sig)
    def add(name, func):
        nonlocal callables
        obj = toObj(func)
        callables.addMethod("number", name, obj)
    def addBool(name, func):
        nonlocal callables, argList
        sig = nativeSig("bool", argList, func)
        obj = object(Type.FUNCTION, sig)
        callables.addMethod("number", name, obj)

    # number operator-(number this)
    def negNum(callables, args):
        val = args[0].data
        return object(Type.NUM, val * -1)
    sig = nativeSig("number", [ "number" ], negNum)
    obj = object(Type.FUNCTION, sig)
    callables.addMethod("number", "operator-", obj)

    # number operator+(number lhs, number rhs)
    def addNums(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.NUM, lhs + rhs)
    add("operator+", addNums)

    # number operator-(number lhs, number rhs)
    def subNums(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.NUM, lhs - rhs)
    add("operator-", subNums)

    # number operator*(number lhs, number rhs)
    def mulNums(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.NUM, lhs * rhs)
    add("operator*", mulNums)

    # number operator/(number lhs, number rhs)
    def divNums(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.NUM, lhs / rhs)
    add("operator/", divNums)

    # bool operator==(number lhs, number rhs)
    def numsEqual(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs == rhs)
    addBool("operator==", numsEqual)

    # bool operator!=(number lhs, number rhs)
    def numsNotEqualTo(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs != rhs)
    addBool("operator!=", numsNotEqualTo)

    # bool operator<(number lhs, number rhs)
    def lessThan(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs < rhs)
    addBool("operator<", lessThan)

    # bool operator>(number lhs, number rhs)
    def greaterThan(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs > rhs)
    addBool("operator>", greaterThan)

    # bool operator<=(number lhs, number rhs)
    def ltEqual(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs <= rhs)
    addBool("operator<=", ltEqual)

    # bool operator>=(number lhs, number rhs)
    def gtEqual(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs >= rhs)
    addBool("operator>=", gtEqual)

    # string ToString()
    def numToString(callables, args):
        this = str(args[0].data)
        return object(Type.STRING, this)
    sig = nativeSig("string", [ "number" ], numToString)
    callables.addMethod("number", "ToString", object(Type.FUNCTION, sig))

    return callables

'''
    string append(string new)
    string operator+(string lhs, string rhs)
    string ToString()
'''
def stdString(callables):
    def splitArgs(args):
        return args[0].data, args[1].data

    # string append(string this, string new)
    def appendStr(callables, args):
        this, new = splitArgs(args)
        this = this + new
        return object(Type.STRING, this)
    sig = nativeSig("string", [ "string", "string" ], appendStr)
    callables.addMethod("string", "append", object(Type.FUNCTION, sig))

    # string operator+(string lhs, string rhs)
    def addStr(callables, args):
        # return lhs.append(rhs)
        method = callables.getMethod("string", "append", "string", [ "string", "string" ])
        return method.call(callables, args)
    sig = nativeSig("string", [ "string", "string" ], addStr)
    callables.addMethod("string", "operator+", object(Type.FUNCTION, sig))
    
    # string ToString(string this)
    def ToString(callables, args):
        return args[0]
    sig = nativeSig("string", [ "string" ], ToString)
    callables.addMethod("string", "ToString", object(Type.FUNCTION, sig))

    return callables

'''
    bool   operator==(bool lhs, bool rhs)
    bool   operator!=(bool lhs, bool rhs)
    string ToString()
'''
def stdBool(callables):
    argList = [ "bool", "bool" ]
    retType = "bool"
    def splitArgs(args):
        return bool(args[0].data), bool(args[1].data)
    def add(name, func):
        nonlocal argList, retType, callables
        sig = nativeSig(retType, argList, func)
        obj = object(Type.FUNCTION, sig)
        callables.addMethod("bool", name, obj)

    # bool operator==(bool lhs, bool rhs)
    def equalTo(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs == rhs)
    add("operator==", equalTo)

    # bool operator!=(bool lhs, bool rhs)
    def notEqualTo(callables, args):
        lhs, rhs = splitArgs(args)
        return object(Type.BOOL, lhs != rhs)
    add("operator!=", notEqualTo)

    # string ToString()
    def boolToString(callables, args):
        _this = bool(args[0].data)
        return object(Type.STRING, str(_this))
    sig = nativeSig(retType, [ "bool" ], boolToString)
    obj = object(Type.FUNCTION, sig)
    callables.addMethod("bool", "ToString", obj)

    return callables





