#
# Seth Gunkel
#

from testUtil import *
from nodes import *
from evaluator import *
from smolParser import *

tests = []
def add(code, result):
    global tests
    tests.append([ code, result])

def check(expected, result, src, func):
    if expected != result:
        report(str(expected), str(result), src, func)
def runAllTests():
    for test in tests:
        code = test[0]
        expected = test[1]
        result = compileAndRun(code).data
        check(expected, result, code, "compileAndRun()")

"""
    Actual tests in the format:
    <code> <result>
"""
add("1", 1)
add("-1", -1)
add("2 + 3", 5)
add("5 - 1", 4)
add("5 * 5", 25)
add("20 / 4", 5)
add("49 / 7 - 1", 6)
add("6 * 9 + -4", 50)
add("-1 + -4", -5)
add("-1 - -5", 4)
add("(2 + 3)", 5)
add("(15 + 13) / 7", 4)
add("8 * (7 / 5)", Decimal("11.2"))
add("(8) + 5 * 4", 28)
add("-(3 * 4)", -12)

# Strings are simply just arrays of immutable strings
add("'Hello World!'", [ 'Hello World!' ])
add("'Hello ' + 'World!'", [ 'Hello ', 'World!' ])

# Boolean
add("true", True)
add("false", False)

# Comparing
add("1 == 1", True)
add("1 == 5", False)
add("1 != 0", True)
add("4 != 4", False)
add("1 - (2 * 3) < 4 == false", False)

# Declaration and Assignment
add("let x = 24", 24)




runAllTests()


