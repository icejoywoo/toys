#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: simple yield demo
    @author: icejoywoo
    @date: 15/12/6
"""


def infinite_increment():
    """ infinite increment by add one
    :return: index
    """
    i = 0
    while 1:
        yield i
        i += 1


for i in infinite_increment():
    print i
    if i > 10:
        break


def even():
    for i in infinite_increment():
        if i % 2 == 0:
            yield i


def multiply(x):
    for i in even():
        yield i * x


for i in multiply(2):
    print i
    if i > 10:
        break