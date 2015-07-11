#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/6

__author__ = 'wujiabin'


def f(x):
    def _f(y):
        def __f(z):
            return x * y * z
        return __f
    return _f


a = f(1)
b = a(2)

print a(3)(4)
print b(3)
