#
# Seth Gunkel
#

from callables import *
from lexer import *
from state import *

class expr:
    def Type(self):
        return "object"
    def ToString(self):
        return "expr"
    def ToStringDebug(self):
        return "<{0}> {1}".format(self.Type(), self.ToString())
    def eval(self, callables, _state = None):
        return object(Type.NIL, None)

class error(expr):
    def __init__(self, msg):
        self.msg = msg
    def ToString(self):
        return self.msg
    def ToStringDebug(self):
        return '<error> "{}"'.format(self.msg)

class number(expr):
    def __init__(self, val):
        self.val = val
    def Type(self):
        return "number"
    def ToString(self):
        return str(self.val)
    def eval(self, callables, _state = None):
        return object(Type.NUM, self.val)

class boolExpr(expr):
    def __init__(self, val):
        self.val = val
    def Type(self):
        return "bool"
    def ToString(self):
        return str(self.val)
    def eval(self, callables, _state = None):
        return object(Type.BOOL, self.val)

class string(expr):
    def __init__(self, _str):
        self.strs = [ _str ]
    def Type(self):
        return "string"
    def ToString(self):
        bigStr = ""
        for _str in self.strs:
            bigStr = bigStr + _str
        return bigStr
    def eval(self, callables, _state = None):
        return object(Type.STRING, self.strs)

class binary(expr):
    def __init__(self, _type, lhs, rhs):
        self.type = _type
        self.lhs  = lhs
        self.rhs  = rhs

    def ToString(self):
        return "({0} {1} {2})".format(self.lhs.ToString(), tokWord[self.type], self.rhs.ToString())

    def ToStringDebug(self):
        return "(<binary> {0} {1} {2})".format(self.lhs.ToStringDebug(), tokWord[self.type], self.rhs.ToStringDebug())

    def eval(self, callables, _state = state(None)):
        lhs = self.lhs.eval(callables, state(_state))
        rhs = self.rhs.eval(callables, state(_state))
        argList    = [ TypeOf(lhs), TypeOf(rhs) ]
        className  = TypeOf(lhs)
        methodName = "operator" + tokWord[self.type]
        method = callables.getMethod(className, methodName, None, argList)
        return method.call(callables, [ lhs, rhs ])

class unary(expr):
    def __init__(self, _type, node):
        self.type = _type
        self.node = node
    
    def ToString(self):
        return "({0}{1})".format(tokWord[self.type], self.node.ToString())

    def ToStringDebug(self):
        return "(<unary> {0}{1})".format(tokWord[self.type], self.node.ToString())

    def eval(self, callables, _state = state(None)):
        this = self.node.eval(callables, _state)
        argList = [ TypeOf(this) ]
        className = TypeOf(this)
        methodName = "operator" + tokWord[self.type]
        method = callables.getMethod(className, methodName, None, argList)
        return method.call(callables, [ this ])

class declaration(expr):
    def __init__(self, name, _expr):
        self.name = name
        self.expr = _expr
    def Type(self):
        return self.expr.Type()
    def ToString(self):
        return "(let {0} = {1})".format(self.name, self.expr.ToString())
    def ToStringDebug(self):
        return "(<declaration> let {0} = {1})".format(self.name, self.expr.ToStringDebug())
    def eval(self, callables, _state = state(None)):
        result = self.expr.eval(callables, _state)
        _state.add(self.name, result)
        return result

class variable(expr):
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
    def Type(self):
        return self.type
    def ToStringDebug(self):
        return "(<variable> {})".format(self.name)
    def eval(self, callables, _state = state(None)):
        return _state.getById(self.name)

class stmt(expr):
    pass

class If(stmt):
    def __init__(self, cond, then, elseThen):
        self.cond = cond
        self.then = then
        self.elseThen = elseThen

class block(stmt):
    def __init__(self, stmts):
        self.stmts = stmts
    def ToStringDebug(self):
        _str = "<block>\n"
        for stmt in self.stmts:
            _str = _str + "  " + stmt.ToStringDebug() + '\n'
        return _str
    def eval(self, callables, _state = state(None)):
        result = None
        for stmt in self.stmt:
            result = stmt.eval(callables, _state)
        return result





