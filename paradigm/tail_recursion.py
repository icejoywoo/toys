#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/6

__author__ = 'wujiabin'


def fact1(n):
    """ normal factorial's recursion version
    :param n:
    :return: factorial n
    """
    if n == 0:
        return 1
    else:
        return n * fact1(n-1)


def fact2(n):
    """ factorial's tail recursion version
    python not support tail recursion elimination
    :param n:
    :return: factorial n
    """

    def aux(n, acc):
        if n == 0:
            return acc
        else:
            return aux(n-1, acc*n)

    return aux(n, 1)


def fact3(n):
    """ real tail recursion in python
    manually eliminate the recursion with a transformation
    http://stackoverflow.com/questions/13591970/does-python-optimize-tail-recursion
    :param n:
    :return:
    """
    acc = 1
    while True:
        if n == 0:
            return acc
        n, acc = n-1, acc*n


#print fact1(1024)
#print fact2(1024)
print fact3(1024)
