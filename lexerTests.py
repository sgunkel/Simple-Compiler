#
# Seth Gunkel
#

from random import *
from lexer import *
from testUtil import *

# Out nice helpers
def tokCmp(tok1, tok2):
    return tok1.type == tok2.type and tok1.word == tok2.word
def errList(expected, result, count):
    print("{0:<20}     Result".format("Expected"))
    for _ in range(0, count - 1):
        print("{0} == {1}".format(expected.pop(0), result.pop(0)))
    print("{0} != {1}".format(expected.pop(), result.pop()))
def check(expected, result, code, func):
    if type(expected) != type(result):
        print("check({0}, {1})".format(type(expected), type(result)), end="")
        print(" Types are not the same.")
        return False

    if isinstance(expected, list):
        if len(expected) != len(result):
            print("Token lengths not equal.")
            report(str(len(expected)), str(len(result)))
            return False
        orig = result.copy()
        for tok in expected:
            if not check(tok, result.pop(0), code, func):
                count = len(orig) - len(result)
                errList(expected, orig, count)
                return False
    else:
        if not tokCmp(expected, result):
            report(expected, result, code, func)
            return False
    return True

"""
  ========================================
  White space (vertical and horizontal)
  ========================================
"""
def singleSpace():
    test = ' '
    expected = token(tokType.WHITESPACEH, '1')
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleSpace)
singleSpace()

def singleTab():
    test = '\t'
    expected = token(tokType.WHITESPACEH, '4')
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleTab)
singleTab()

def singleNewLine():
    test = '\n'
    expected = token(tokType.WHITESPACEV, '1')
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleNewLine)
singleNewLine()

def multipleSpace():
    num = randint(1, 20)
    test = ' ' * num
    expected = token(tokType.WHITESPACEH, str(num))
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, multipleSpace)
multipleSpace()

def multipleTab():
    num = randint(1, 20)
    test = '\t' * num
    expected = token(tokType.WHITESPACEH, str(num * 4))
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, multipleTab)
multipleTab()

def multipleNewLine():
    num = randint(1, 20)
    test = '\n' * num
    expected = token(tokType.WHITESPACEV, str(num))
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, multipleNewLine)
multipleNewLine()

def mixedWhiteSpace():
    test = "  \n\n\n\t \t\n"
    expected = [
        token(tokType.WHITESPACEH, '2'),
        token(tokType.WHITESPACEV, '3'),
        token(tokType.WHITESPACEH, '9'),
        token(tokType.WHITESPACEV, '1')
    ]
    driver = lexer(test)
    result = []
    while driver.cur() != None:
        result.append(driver.getTok())
    check(expected, result, test, mixedWhiteSpace)
mixedWhiteSpace()

"""
    End of file
"""
def eofTest():
    test = ""
    expected = token(tokType.EOF)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, eofTest)
eofTest()

"""
  ========================================
   Number (with and without a decimal place)
  ========================================
"""
def singleDigit():
    num = randint(0, 9)
    test = str(num)
    expected = token(tokType.NUM, str(num))
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleDigit)
singleDigit()

def bigWholeNumber():
    num = randint(1000, 10000)
    test = str(num)
    expected = token(tokType.NUM, str(num))
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleDigit)
bigWholeNumber()

def dot():
    test = '.'
    expected = token(tokType.DOT)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, dot)
dot()

def dotDotDot():
    test = "..."
    expected = [
        token(tokType.DOT),
        token(tokType.DOT),
        token(tokType.DOT)
    ]
    driver = lexer(test)
    result = []
    while driver.cur() != None:
        result.append(driver.getTok())
    check(expected, result, test, dotDotDot)
dotDotDot()

def numWithDecimal():
    # <randint> '.' <randint>
    right = randint(1, 50)
    left = randint(1, 50)
    test = "{0}.{1}".format(str(left), str(right))
    expected = [
        token(tokType.NUM, str(left)),
        token(tokType.DOT),
        token(tokType.NUM, str(right))
    ]
    driver = lexer(test)
    result = []
    while driver.cur() != None:
        result.append(driver.getTok())
    check(expected, result, test, numWithDecimal)
numWithDecimal()

def numPostDecimal():
    # '.' <randint>
    num = randint(1, 50)
    test = ".{}".format(str(num))
    expected = [
        token(tokType.DOT),
        token(tokType.NUM, str(num))
    ]
    driver = lexer(test)
    result = []
    while driver.cur() != None:
        result.append(driver.getTok())
    check(expected, result, test, numPostDecimal)
numPostDecimal()

def invalidNum():
    # <randint> '.'
    num = randint(100, 10000)
    test = "{}.".format(str(num))
    expected = [
        token(tokType.NUM, str(num)),
        token(tokType.DOT)
    ]
    driver = lexer(test)
    result = []
    while driver.cur() != None:
        result.append(driver.getTok())
    check(expected, result, test, invalidNum)
invalidNum()

"""
  ========================================
  String
  ========================================
"""
def emptyString():
    test = "''"
    expected = token(tokType.STR, "")
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, emptyString)
emptyString()

def singleChar():
    test = "'x'"
    expected = token(tokType.STR, "x")
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleChar)
singleChar()

def fullSentance():
    sentance = "The quick brown fox jumps over the lazy dog"
    test = '"{}"'.format(sentance)
    expected = token(tokType.STR, sentance)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, fullSentance)
fullSentance()

def stringInString():
    sentance = 'Every programmer writes a "Hello World!" program for good luck.'
    test = "'{}'".format(sentance)
    expected = token(tokType.STR, sentance)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, stringInString)
stringInString()

def boolTrue():
    test = "true"
    expected = token(tokType.BOOL, "true")
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, boolTrue)
boolTrue()

def boolFalse():
    test = "false"
    expected = token(tokType.BOOL, "false")
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, boolFalse)
boolFalse()

def singleCharID():
    test = 'x'
    expected = token(tokType.ID, 'x')
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, singleCharID)
singleCharID()

def wordID():
    test = "word"
    expected = token(tokType.ID, "word")
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, wordID)
wordID()

"""
  ========================================
  Operators
  ========================================
"""
def plusSign():
    test = '+'
    expected = token(tokType.PLUS)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, plusSign)
plusSign()

def minusSign():
    test = '-'
    expected = token(tokType.MINUS)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, minusSign)
minusSign()

def starSign():
    test = '*'
    expected = token(tokType.STAR)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, starSign)
starSign()


def slashSign():
    test = '/'
    expected = token(tokType.SLASH)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, slashSign)
slashSign()

def assign():
    test = "="
    expected = token(tokType.ASSIGN)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, assign)
assign()

def equalTo():
    test = "=="
    expected = token(tokType.EQUAL_TO)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, equalTo)
equalTo()

def equalToWithSpace():
    test = " == "
    expected = token(tokType.EQUAL_TO)
    driver = lexer(test)
    result = driver.next()
    check(expected, result, test, equalToWithSpace)
equalToWithSpace()

def notEqualTo():
    test = "!="
    expected = token(tokType.NOT_EQUAL_TO)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, notEqualTo)
notEqualTo()

def lessThan():
    test = '<'
    expected = token(tokType.LESS_THAN)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, lessThan)
lessThan()

def greaterThan():
    test = '>'
    expected = token(tokType.GREATER_THAN)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, greaterThan)
greaterThan()

def lessThanEqual():
    test = "<="
    expected = token(tokType.LT_EQUAL)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, lessThanEqual)
lessThanEqual()

def greaterThanEqual():
    test = ">="
    expected = token(tokType.GT_EQUAL)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, greaterThanEqual)
greaterThanEqual()

def openParen():
    test = '('
    expected = token(tokType.OPEN_PAREN)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, openParen)
openParen()

def closeParen():
    test = ')'
    expected = token(tokType.CLOSE_PAREN)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, closeParen)
closeParen()

"""
    Keywords
"""
def let():
    test = "let"
    expected = token(tokType.LET)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, let)
let()

def If():
    test = "if"
    expected = token(tokType.IF)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, If)
If()

def Else():
    test = "else"
    expected = token(tokType.ELSE)
    driver = lexer(test)
    result = driver.getTok()
    check(expected, result, test, Else)
Else()



