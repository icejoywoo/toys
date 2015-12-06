#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 15/12/6
"""

import re

import perf

s = ("Note that there is a significant advantage in Python to adding a number "
     "to itself instead of multiplying it by two or shifting it left by one bit. "
     "In C on all modern computer architectures, each of the three arithmetic "
     "operations are translated into a single machine instruction which executes "
     "in one cycle, so it doesn't really matter which one you choose.")

words = re.split(r'\W', s)


def string_add():
    r = ''
    for w in words:
        r += w + ' '
    return r


def string_join():
    return ' '.join(words)


if __name__ == '__main__':
    print perf.perf(string_add)
    print perf.perf(string_join)

