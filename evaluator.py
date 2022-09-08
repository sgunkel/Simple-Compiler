#
# Seth Gunkel
#
from nodes import *
from smolParser import *

# might not need below...
class memBank:
    def __init__(self, prev):
        self.stack = { } # name : value (object)
        self.prev = prev
        self.next = None
    def isParent(self):
        return self.prev == None
    def get(self, name):
        if name in self.stack:
            return self.stack[name]
        elif self.isParent():
            # might do some error handling here..
            return None
        return self.prev.get(name)


callables = newCallables()
# callables.stringView() # Prints all defined functions and methods to stdout.
def evaluate(root):
    #result = ToString(callables, root.eval(callables))
    #print(result.data)
    return root.eval(callables)

def compile(code):
    _parser = parser(code)
    return _parser.run()

def compileAndRun(code):
    return evaluate(compile(code))




