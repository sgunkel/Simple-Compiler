#
# Seth Gunkel
#

from object import *
from signatures import *
from stdTypes import *

# Native and user defined functions.
# To run a function, whether native or user defined,
#   you would use the 'call' method, passing it
#   callables (to run other functions inside) and
#   an array of objects for the arguments.
'''class signature:
    def __init__(self, retType, argList):
        self.retType = retType
        self.argList = argList
    def call(self, callables, args):
        pass
class smolSig(signature):
    def __init__(self, retType, argList, code):
        super().__init__(retType, argList)
        self.code = code
    def call(callables, args):
        return self.code.accept(callables)
class nativeSig(signature):
    def __init__(self, retType, argList, code):
        super().__init__(retType, argList)
        self.code = code
    def call(self, callables, args):
        return self.code(callables, args)
'''

"""
  The callables class holds all callable code
  (functions) for easy retrieval. This holds both
  functions and methods and provides 4 methods to
  access them:
    getFunctionObj(name, retType, argList)
    getMethodObj(className, name, retType, argList)
      Above both return an 'object' that holds the
      code.
    getFunction(name, retType, argList)
    getMethod(className, name, retType, argList)
      Above both return a 'signature' to which you
      can run the code with the 'call' method.
"""
class callables:
    def __init__(self):
        self.funcs = {} # funcName : object[]
        self.methods = {} # className : { funcName : object[] }

    def addFunc(self, name, sig):
        if name not in self.funcs:
            self.funcs[name] = []
        self.funcs[name].append(sig)

    def addMethod(self, className, name, sig):
        if className not in self.methods:
            self.methods[className] = {}
        if name not in self.methods[className]:
            self.methods[className][name] = []
        self.methods[className][name].append(sig)

    def _getFuncObjs(self, name):
        if name not in self.funcs:
            return None # might use 'exit(-1)'..?
        return self.funcs[name]

    def _getMethObjs(self, className, name):
        if className in self.methods:
            if name in self.methods[className]:
                return self.methods[className][name]
        return None

    def _getFromList(self, objs, retType, argList):
        if objs == None: return None
        for obj in objs:
            sig = obj.data
            if sig.argList == argList:
                if retType == None or sig.retType == retType:
                    return obj
        return None

    def getFunctionObj(self, name, retType, argList):
        return self._getFromList(self._getFuncObjs(name), retType, argList)

    def getMethodObj(self, className, name, retType, argList):
        return self._getFromList(self._getMethObjs(className, name), retType, argList)

    def getFunction(self, name, retType, argList):
        obj = self.getFunctionObj(name, retType, argList)
        if obj == None: return None
        return obj.data

    def getMethod(self, className, name, retType, argList):
        obj = self.getMethodObj(className, name, retType, argList)
        if obj == None: return None
        return obj.data
    # Prints the whole structure - for debugging.
    def stringView(self):
        def argsToString(args):
            _str = ""
            for i in range(0, len(args)):
                if i == 0 or i == len(args):
                    _str = _str + args[i]
                else:
                    _str = _str + ", {}".format(args[i])
            return _str
        def printFunc(className, funcName, sig):
            if className != "": className = className + '::'
            print("{0} {1}{2}({3})".format(sig.retType, className, funcName, argsToString(sig.argList)))

        print("Defined functions:")
        for funcName in self.funcs:
            for obj in self.funcs[funcName]:
                sig = obj.data
                printFunc("", funcName, sig)
        print("Defined methods:")
        for className in self.methods:
            for funcName in self.methods[className]:
                for obj in self.methods[className][funcName]:
                    sig = obj.data
                    printFunc(className, funcName, sig)

def ToString(callables, obj):
    className = TypeOf(obj)
    method = callables.getMethod(className, "ToString", None, [ TypeOf(obj) ])
    if method == None:
       return object(Type.STRING, "<{}>".format(className))
    return method.call(callables, [ obj ])

def newCallables():
    _callables = callables()
    _callables = stdNumber(_callables)
    _callables = stdString(_callables)
    _callables = stdBool(_callables)
    #_callables.stringView()
    return _callables

'''
# quick function test
retType = "number"
argList = [ "number", "number" ]
def addNumsFunc(callables, args):
    lhs = int(args[0].data)
    rhs = int(args[1].data)
    return object(Type.NUM, lhs + rhs)
addNumsSig = nativeSig(retType, argList, addNumsFunc)
addNumsObj = object(Type.FUNCTION, addNumsSig)
c = callables()
c.addFunc("addNums", addNumsObj)

lhs = object(Type.NUM, 1)
rhs = object(Type.NUM, 1)
func = c.getFunction("addNums", None, [ "number", "number" ])
print("Function 'addNums'")
print(func)
obj = func.call(c, [ lhs, rhs ])
print(obj)
print(obj.type)
print(obj.data)

# quick method test
c.addMethod("number", "operator+", addNumsObj)
method = c.getMethod("number", "operator+", None, argList)
obj = method.call(c, [ lhs, rhs ])
print("Method 'number.operator+'")
print(method)
print(obj)
print(obj.type)
print(obj.data)
'''




