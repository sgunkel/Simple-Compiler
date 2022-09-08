"""
Source:
https://gist.github.com/igstan/2fe9bd63beaf411292a2
"""

class Expr(object):
    def accept(self, visitor):
        method_name = 'visit_{}'.format(self.__class__.__name__.lower())
        visit = getattr(visitor, method_name)
        return visit(self)


class Int(Expr):
    def __init__(self, value):
        self.value = value


class Add(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Mul(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Visitor(object):
    pass


class Eval(Visitor):
    def visit_int(self, i):
        return i.value

    def visit_add(self, a):
        return a.left.accept(self) + a.right.accept(self)

    def visit_mul(self, a):
        return a.left.accept(self) * a.right.accept(self)


class Print(Visitor):
    def visit_int(self, i):
        return i.value

    def visit_add(self, a):
        return '(+ {} {})'.format(a.left.accept(self), a.right.accept(self))

    def visit_mul(self, a):
        return '(* {} {})'.format(a.left.accept(self), a.right.accept(self))


class CaseVisitor(Visitor):
    def __init__(self, int_case, add_case, mul_case):
        self.int_case = int_case
        self.add_case = add_case
        self.mul_case = mul_case

    def visit_int(self, i):
        return self.int_case(i)

    def visit_add(self, a):
        return self.add_case(a)

    def visit_mul(self, a):
        return self.mul_case(a)


def eval(ast):
    def int_case(n):
        return n.value
    def add_case(n):
        return eval(n.left) + eval(n.right)
    def mul_case(n):
        return eval(n.left) * eval(n.right)
    return ast.accept(CaseVisitor(int_case, add_case, mul_case))


def eval2(ast):
    return ast.accept(CaseVisitor(
        int_case = lambda n: n.value,
        add_case = lambda n: eval(n.left) + eval(n.right),
        mul_case = lambda n: eval(n.left) * eval(n.right)
    ))


def main():
    expr = Add(Add(Int(4), Int(3)), Mul(Int(10), Add(Int(1), Int(1))))
    print(expr.accept(Print()))
    print(expr.accept(Eval()))
    print(eval(expr))


if __name__ == '__main__':
    main()
