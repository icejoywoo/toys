#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/6

__author__ = 'wujiabin'


from patterns import patterns

@patterns
def factorial():
    if 0: 1
    if n is int: n * factorial(n-1)
    if []: []
    if [x] + xs: [factorial(x)] + factorial(xs)
    if {'n': n, 'f': f}: f(factorial(n))

assert factorial(0) == 1
assert factorial(5) == 120
assert factorial([3, 4, 2]) == [6, 24, 2]
assert factorial({'n': [5, 1], 'f': sum}) == 121

print factorial({'n': 4, 'f': lambda x: x * 3})
factorial('hello')  # raises Mismatch
