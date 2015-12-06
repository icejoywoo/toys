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

words_list = re.split(r'\W', s)
words_tuple = tuple(words_list)
words_dict = dict.fromkeys(words_list, None)
words_set = set(words_list)


l = ('there', 'is', 'python', 'jason', 'hello', 'hill', 'with', 'phone', 'test',
     'dfdf', 'apple', 'pdf', 'in', 'basic', 'none', 'advantage', 'var', 'bana')


def in_string():
    f = []
    for i in l:
        if i not in s:
            f.append(i)
    return f


def in_list():
    f = []
    for i in l:
        if i not in words_list:
            f.append(i)
    return f


def in_tuple():
    f = []
    for i in l:
        if i not in words_tuple:
            f.append(i)
    return f


def in_dict():
    f = []
    for i in l:
        if i not in words_dict:
            f.append(i)
    return f


def in_set():
    f = []
    for i in l:
        if i not in words_set:
            f.append(i)
    return f


if __name__ == '__main__':
    print perf.perf(in_string)

    print perf.perf(in_list)
    print perf.perf(in_tuple)

    print perf.perf(in_dict)
    print perf.perf(in_set)
