#
# Seth Gunkel
#

from enum import Enum, auto

class tokType(Enum):

    # Built-in types
    NUM   = auto()
    STR   = auto()
    ID    = auto()
    BOOL  = auto()

    # Binary
    PLUS   = auto()
    MINUS  = auto()
    STAR   = auto()
    SLASH  = auto()
    ASSIGN = auto()

    # Comparisions (binary)
    EQUAL_TO     = auto()
    NOT_EQUAL_TO = auto()
    LESS_THAN    = auto()
    GREATER_THAN = auto()
    LT_EQUAL     = auto() # Shorter naming.
    GT_EQUAL     = auto() # ^^

    DOT = auto()

    # Keywords
    LET  = auto()
    IF   = auto()
    ELSE = auto()

    # Unary
    NEGATE = auto()
    NOT    = auto()

    # Grouping
    OPEN_PAREN  = auto()
    CLOSE_PAREN = auto()

    # Whitespace
    WHITESPACEV = auto() # vertical
    WHITESPACEH = auto() # horizontal

    EOF = auto()

# Helps in processing two character operators like
#   "==", "!=", etc.
# Format: <starting char> : [ <ending char>, <token type> ]
startingTwoCharOPs = {
    '!': [ '=', tokType.NOT_EQUAL_TO ],
    '=': [ '=', tokType.EQUAL_TO ],
    '<': [ '=', tokType.LT_EQUAL ],
    '>': [ '=', tokType.GT_EQUAL ],
}

# Helps in transforming words into their tokens.
wordTok = {
    '+': tokType.PLUS,
    '-': tokType.MINUS,
    '*': tokType.STAR,
    '/': tokType.SLASH,
    '.': tokType.DOT,
    '(': tokType.OPEN_PAREN,
    ')': tokType.CLOSE_PAREN,
    '!': tokType.NOT,
    '=': tokType.ASSIGN,
    '>': tokType.GREATER_THAN,
    '<': tokType.LESS_THAN,

    '==': tokType.EQUAL_TO,
    '!=': tokType.NOT_EQUAL_TO,
    '<=': tokType.LT_EQUAL,
    '>=': tokType.GT_EQUAL,

    # Keywords.
    "true":  tokType.BOOL,
    "false": tokType.BOOL,
    "let":   tokType.LET,
    "if":    tokType.IF,
    "else":  tokType.ELSE,
}
tokWord = dict([(value, key) for key, value in wordTok.items()])
tokWord[tokType.NEGATE] = '-'

class token:
    def __init__(self, _type, _word = ''):
        self.type = _type
        self.word = _word

    def __str__(self):
        return "{0:<20}{1}".format(self.type, self.word)

class lexer:
    def __init__(self, src):
        self.code = src
        self.pos  = 0

    def cur(self):
        if self.pos >= len(self.code):
            return None
        return self.code[self.pos]

    def upPos(self):
        self.pos = self.pos + 1

    # "==", "!=", etc.
    def toTwoCharOP(self, word):
        if word in startingTwoCharOPs:
            if startingTwoCharOPs[word][0] == self.cur():
                self.upPos() # eat the second character of the operator.
                _type = startingTwoCharOPs[word][1]
                return token(_type)
        return None

    def wordToTok(self, word):
        if word == None:
            return token(tokType.EOF)
        elif word in [ "true", "false" ]:
            return token(tokType.BOOL, word)
        elif word in wordTok:
            tok = self.toTwoCharOP(word)
            if tok != None:
                return tok
            return token(wordTok[word])
        return token(tokType.ID, word)

    def getTok(self):
        # Whitespace
        if self.cur() in ['\n', '\t', ' ']:
            count = 0
            if self.cur() == '\n':
                while self.cur() == '\n':
                    count = count + 1
                    self.upPos()
                return token(tokType.WHITESPACEV, str(count))
            while self.cur() in ['\t', ' ']:
                if self.cur() == '\t':
                    count = count + 3
                count = count + 1
                self.upPos()
            return token(tokType.WHITESPACEH, str(count))
        # Number
        elif str(self.cur()).isdigit():
            num = self.cur()
            while True:
                self.upPos()
                if not str(self.cur()).isdigit():
                    break
                num = num + self.cur()
            return token(tokType.NUM, num)
        # String
        elif self.cur() in [ "'", '"' ]:
            _str = ""
            end = self.cur()
            while True:
                self.upPos()
                if self.cur() in [ None, end ]:
                    if self.cur() == end:
                        self.upPos()
                    break
                _str = _str + self.cur()
            return token(tokType.STR, _str)

        # === Get the whole word and process it ===
        word = self.cur()
        while True:
            self.upPos()
            if self.cur() == None or not self.cur().isalpha():
                break
            word = word + self.cur()

        # Identifier or keywords.
        return self.wordToTok(word)

    # Gets the next token WITHOUT whitespace.
    def next(self):
        while True:
            tok = self.getTok()
            if tok == None:
                return None
            elif tok.type not in [ tokType.WHITESPACEV, tokType.WHITESPACEH ]:
                return tok
