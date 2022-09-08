#
# Seth Gunkel
#

from testUtil import *
from smolParser import *
from random import randint, uniform

count = 0
def check(expected, result, code, func):
    global count
    count = count + 1
    if type(expected) != type(result):
        print("Type mismatch: {0} {1}".format(type(expected), type(result)))
        print(code)
        print(func)
        return False
    elif isinstance(expected, expr):
        if expected.ToStringDebug() != result.ToStringDebug():
            report(expected.ToStringDebug(), result.ToStringDebug(), code, func)
    else:
        return False
    return True

"""
  Built-in types.
"""
def numExpr():
    num = randint(0, 100)
    test = str(num)
    expected = number(num)
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numExpr)
numExpr()

def numDecimal():
    num = uniform(0.0, 100.0)
    test = str(num)
    expected = number(num)
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numDecimal)
numDecimal()

def numInvalidDecimal():
    num = randint(0, 100)
    test = str(num) + '.'
    expected = error("Expected a number after decimal place.")
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numInvalidDecimal)
numInvalidDecimal()

def emptyString():
    test = '""'
    expected = string("")
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, emptyString)
emptyString()

def fullString():
    sentance = "Hello World!"
    test = "'{}'".format(sentance)
    expected = string(sentance)
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, fullString)
fullString()

def stringConcat():
    word1 = "Hello "
    word2 = "World!"
    test = "'{0}' + '{1}'".format(word1, word2)
    expected = binary(tokType.PLUS, string(word1), string(word2))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, stringConcat)
stringConcat()

def boolTrue():
    test = "true"
    expected = boolExpr(True)
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, boolTrue)
boolTrue()

def boolFalse():
    test = "false"
    expected = boolExpr(False)
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, boolFalse)
boolFalse()

"""
    Unary expressions
"""
def negateNum():
    num = randint(1, 100)
    test = "-{}".format(num)
    expected = unary(tokType.NEGATE, number(num))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, negateNum)
negateNum()

"""
    Binary expressions
"""
def numberAddition():
    lhs = randint(0, 100)
    rhs = randint(0, 100)
    test = "{0} + {1}".format(lhs, rhs)
    expected = binary(tokType.PLUS, number(lhs), number(rhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numberAddition)
numberAddition()

def numberSubtraction():
    lhs = randint(0, 100)
    rhs = randint(0, 100)
    test = "{0} - {1}".format(lhs, rhs)
    expected = binary(tokType.MINUS, number(lhs), number(rhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numberSubtraction)
numberSubtraction()

def numberMultiplication():
    lhs = randint(0, 100)
    rhs = randint(0, 100)
    test = "{0} * {1}".format(lhs, rhs)
    expected = binary(tokType.STAR, number(lhs), number(rhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numberMultiplication)
numberMultiplication()

def numberDivision():
    lhs = randint(0, 100)
    rhs = randint(0, 100)
    test = "{0} / {1}".format(lhs, rhs)
    expected = binary(tokType.SLASH, number(lhs), number(rhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numberDivision)
numberDivision()

def lhsNegate():
    lhs = randint(-100, -1)
    rhs = randint(1, 100)
    test = "{0} + {1}".format(lhs, rhs)
    expected = binary(tokType.PLUS, unary(tokType.NEGATE, number(lhs * -1)), number(rhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, lhsNegate)
lhsNegate()

def rhsNegate():
    lhs = randint(0, 100)
    rhs = randint(-100, -1)
    test = "{0} + {1}".format(lhs, rhs)
    expected = binary(tokType.PLUS, number(lhs), unary(tokType.NEGATE, number(rhs * -1)))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, rhsNegate)
rhsNegate()

def bothHandSideNegated():
    lhs = randint(-100, -1)
    rhs = randint(-100, -1)
    test = "{0} + {1}".format(lhs, rhs)
    expected = binary(tokType.PLUS, unary(tokType.NEGATE, number(lhs * -1)), unary(tokType.NEGATE, number(rhs * -1)))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, bothHandSideNegated)
bothHandSideNegated()

def numsEqualTo():
    num = randint(0, 100)
    test = "{0} == {0}".format(num)
    expected = binary(tokType.EQUAL_TO, number(num), number(num))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numsEqualTo)
numsEqualTo()

def numsNotEqualTo():
    num = randint(0, 100)
    test = "{0} != {0}".format(num)
    expected = binary(tokType.NOT_EQUAL_TO, number(num), number(num))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, numsNotEqualTo)
numsNotEqualTo()

def declareVariable():
    test = "let x = 42"
    expected = declaration('x', number(42))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, declareVariable)
declareVariable()


"""
  ========================================
  Precedence
  ========================================
"""
def addMultiply():
    llhs = randint(0, 100)
    lrhs = randint(0, 100)
    rrhs = randint(0, 100)
    test = "{0} + {1} * {2}".format(llhs, lrhs, rrhs)
    expected = binary(tokType.PLUS, number(llhs), binary(tokType.STAR, number(lrhs), number(rrhs)))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, addMultiply)
addMultiply()

def multiplyAdd():
    llhs = randint(0, 100)
    lrhs = randint(0, 100)
    rrhs = randint(0, 100)
    test = "{0} * {1} + {2}".format(llhs, lrhs, rrhs)
    expected = binary(tokType.PLUS, binary(tokType.STAR, number(llhs), number(lrhs)), number(rrhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, multiplyAdd)
multiplyAdd()

def subtractDivide():
    llhs = randint(0, 100)
    lrhs = randint(0, 100)
    rrhs = randint(0, 100)
    test = "{0} - {1} / {2}".format(llhs, lrhs, rrhs)
    expected = binary(tokType.MINUS, number(llhs), binary(tokType.SLASH, number(lrhs), number(rrhs)))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, subtractDivide)
subtractDivide()

"""
    Grouping
"""
def lhsParen():
    llhs = randint(1, 100)
    lrhs = randint(1, 100)
    rrhs = randint(1, 100)
    test = "({0} + {1}) * {2}".format(llhs, lrhs, rrhs)
    expected = binary(tokType.STAR, binary(tokType.PLUS, number(llhs), number(lrhs)), number(rrhs))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, lhsParen)
lhsParen()

def negateWholeExpr():
    lhs = randint(1, 100)
    rhs = randint(1, 100)
    test = "-({0} + {1})".format(lhs, rhs)
    expected = unary(tokType.NEGATE, binary(tokType.PLUS, number(lhs), number(rhs)))
    driver = parser(test)
    result = driver.run()
    check(expected, result, test, negateWholeExpr)
negateWholeExpr()
    





