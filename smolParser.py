#
# Seth Gunkel
#

from lexer import *
from nodes import *

# Precedence levels for operators.
prec = {
    tokType.ASSIGN : 5,
    tokType.EQUAL_TO : 10,
    tokType.NOT_EQUAL_TO : 10,
    tokType.GREATER_THAN : 10,
    tokType.LESS_THAN : 10,
    tokType.GT_EQUAL : 10,
    tokType.LT_EQUAL : 10,
    tokType.PLUS : 20,
    tokType.MINUS : 20,
    tokType.STAR : 30,
    tokType.SLASH : 30,
    tokType.NEGATE : 40,
    tokType.NOT : 40,
}
def getPrec(_type):
    if _type in prec:
        return prec[_type]
    return -1

class parser:
    def __init__(self, src):
        self.lexie = lexer(src)
        self.cur   = self.lexie.getTok()
        self.next  = None

        self.indentLevel = 0

    # Our nice helpers.
    def peek(self):
        return self.cur
    def peekNext(self):
        if self.next is None:
            self.next = self.lexie.getTok()
        return self.next
    def consume(self, whitespace = False):
        if self.next is None:
            if whitespace:
                self.cur = self.lexie.getTok()
            else:
                self.cur = self.lexie.next()
        else:
            self.cur = self.next
            self.next = None

    def run(self):
        return self._stmt()

    """
    stmt := ifStmt
            expr <new line>
    """
    def _stmt(self):
        return self._expr()

    """
    ifStmt := 'if' ('(')? expr (')') next stmt ('else' stmt)?
    next := <indention> <new line>
    """
    def _ifStmt(self):
        hasParens = Fasle
        self.consume() # 'if'

        # Possibly an opening parentheses.
        cur = self.peek()
        if cur.type == tokType.OPEN_PAREN:
            hasParens = True
            self.consume() # '('

        # Condition
        cond = self._expr()
        if cond == None:
            # error
            return None

        # Possible a closing parentheses.
        cur = self.peek()
        if hasParens:
            if cur.type != tokType.CLOSING_PAREN:
                # error
                return None
            self.consume() # ')'

        thenBlock = self._block()

        # Check for else block.
        elseBlock = None
        cur = self.peek()
        if cur.type == tokType.ELSE:
            pass
        return If(cond, thenBlock, elseBlock)
    # above has not been tested yet..


    """
        primary := number      |
                   string      |
                   bool        |
                   unary       |
                   paren       |
                   declaration
    """
    def _primary(self):
        cur = self.peek()
        if cur.type == tokType.NUM:
            return self._numExpr()
        elif cur.type == tokType.STR:
            return self._string()
        elif cur.type == tokType.BOOL:
            return self._bool()
        elif cur.type in [ tokType.MINUS, tokType.NOT ]:
            return self._unary()
        elif cur.type == tokType.OPEN_PAREN:
            return self._paren()
        elif cur.type == tokType.LET:
            return self._declaration()
        # report error and panic
        return None

    """
        paren := '(' expr ')'
    """
    def _paren(self):
        self.consume() # eat the '('
        expr = self._expr()
        if expr == None:
            return None # error
        elif self.peek().type != tokType.CLOSE_PAREN:
            return None # error
        self.consume() # eat the ')'
        return expr

    """
        binary := primary op*
        op     := '+' | '-' | '/' | '*'
    """
    def _binary(self, exprPrec, lhs):
        while True:
            prec = getPrec(self.peek().type)

            # Either not an operator, or the given
            #   operator has less precedence.
            if prec < exprPrec:
                return lhs

            # The operator.
            op = self.peek().type
            self.consume() # eat the operator

            # Right side of the expression.
            rhs = self._primary()
            if rhs == None:
                # report error and panic
                return None

            nextPrec = getPrec(self.peek().type)
            if prec < nextPrec:
                rhs = self._binary(prec + 1, rhs)
                if rhs == None:
                    return None

            # The next binary expression.
            lhs = binary(op, lhs, rhs)

    """
        expr := primary |
                binary
    """
    def _expr(self):
        lhs = self._primary()
        if lhs == None:
            # report error and panic
            return None
        return self._binary(0, lhs)

    """
        unary := op primary
        op    := '-' | '!'
    """
    def _unary(self):
        sign = self.peek().type
        self.consume() # eat the operator

        # Change the '-' prec level to a higher one.
        if sign == tokType.MINUS:
            sign = tokType.NEGATE
        rhs = self._primary()
        if rhs == None:
            # report error and panic
            return None
        return unary(sign, rhs)

    """
        number := digits | digits '.' digits
        digits := digit*
        digit  := [0-9]
    """
    def _numExpr(self):
        """
        3.145
        ^^^
        || ` Mantissa
        | ` Decimal
         ` Unit
        """
        unit = int(self.peek().word)
        num = unit
        self.consume() # eat the number (unit)

        # Check for a decimal place.
        if self.peek().type == tokType.DOT:
            self.consume() # eat the decimal
            if self.peek().type != tokType.NUM:
                return error("Expected a number after decimal place.")
            mantissa = float(".{}".format(self.peek().word))
            num = unit + mantissa
            self.consume() # eat the mantissa
        return number(num)

    """
    string := '"' chars* '"' |
              "'" chars* "'"
    chars := char*
    char := *any key*
    """
    def _string(self):
        # do some interpretated string action here..
        _str = string(str(self.peek().word))
        self.consume() # eat the string
        return _str

    """
    bool = "true" | "false"
    """
    def _bool(self):
        word = self.peek().word
        self.consume() # eat the bool value
        return boolExpr(word == "true")

    """
    declaration := "let" id "=" primary
    """
    def _declaration(self):
        self.consume() # 'let'

        name = self.peek().word
        self.consume() # id
        self.consume() # '='

        rhs = self._primary()
        self.consume() # might be wrong

        return declaration(name, rhs)

    """
    block := indention expr*
    indention := ("  " | "    " | "/t")*
    """
    def _block(self):
        exprList = []
        preLevel = self.indentionLevel
        curLevel = self.indentionLevel = int(self.peek().word)
        '''
        ugh, the consume method might be a problem with the whitespaces skipped when running the _primary() method...
        '''
        while True:
            # Indention level.
            cur = self.peek()
            if cur.type != tokType.WHITESPACEH:
                break # end of block or error
            elif int(cur.word) < curLevel:
                break # ending of block
            self.consume(whitespace = True) # indention

            # The expression.
            cur = self._primary()
            if cur == None:
                break
            exprList.append(cur)
            # maybe above can generate a statement and a statement just validates that an expression has a new line..?

            # Check for a new line.
            cur = self.peek()
            if cur != tokType.WHITESPACEV:
                # error - expected a new line
                break
            self.consume(whitespace = True)
        self.indentionLevel = preLevel
        return block(exprList)


