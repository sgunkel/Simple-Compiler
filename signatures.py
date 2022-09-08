#
# Seth Gunkel
#

# Native and user defined functions.
# To run a function, whether native or user defined,
#   you would use the 'call' method, passing it
#   callables (to run other functions inside) and
#   an array of objects for the arguments.
class signature:
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
