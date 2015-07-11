#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/6

__author__ = 'wujiabin'


class Exp(object):
    """ expression
    """
    pass


class Value(Exp):

    def eval(self):
        return self


class Int(Value):

    def __init__(self, i):
        self.i = i

    def __str__(self):
        return str(self.i)

    def __repr__(self):
        return 'Int({})'.format(self.i)

    def add(self, e):
        return e.add_int(self)

    def add_string(self, e):
        return String(str(self) + str(e))

    def add_int(self, e):
        return Int(self.i + e.i)

    def mult(self, e):
        return e.mult_int(self)

    def mult_string(self, e):
        return String(str(e) * self.i)

    def mult_int(self, e):
        return Int(self.i * e.i)


class String(Value):

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return 'String({})'.format(self.s)

    def add(self, e):
        return e.add_string(self)

    def add_string(self, e):
        return String(str(self) + str(e))

    def add_int(self, e):
        return String(str(self) + str(e))

    def mult(self, e):
        return e.mult_string(self)

    def mult_string(self, e):
        raise ValueError("Cannot multiply between strings.")

    def mult_int(self, e):
        return String(str(self) * e.i)


class Negate(Exp):

    def __init__(self, e):
        self.e = e

    def eval(self):
        return Int(-self.e.eval().i)

    def __str__(self):
        return '-({})'.format(self.e)


class Add(Exp):

    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def eval(self):
        return self.e1.eval().add(self.e2.eval())

    def __str__(self):
        return '({0} + {1})'.format(self.e1, self.e2)


class Mult(Exp):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def eval(self):
        return self.e1.eval().mult(self.e2.eval())

    def __str__(self):
        return '({0} * {1})'.format(self.e1, self.e2)


if __name__ == '__main__':
    print Mult(String('abcd'), String('abcd')).eval()  # raise ValueError
    print Int(5).eval()  # >>> 5
    print Negate(Add(Int(5), Int(3))).eval()  # >>> -8
    print Add(Negate(Int(5)), Int(6)).eval()  # >>> 1
    print Negate(Mult(Negate(Int(5)), Int(6))).eval()  # >>> 30
    print Mult(Int(5), String('abcd')).eval()  # >>> 'abcdabcdabcdabcdabcd'
