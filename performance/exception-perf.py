#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 15/12/6
"""

import perf


dict_string = "A 10\nB 20\nD 5"


def query_wrapper():
    not_init = True

    def wrapper(k):
        if not_init:
            # simulate loading dict file
            d = dict([line.split() for line in dict_string.split('\n')])
        return d.get(k, None)

    return wrapper

query = query_wrapper()


def query_wrapper_e():
    d = [None]

    def wrapper(k):
        try:
            return d[0].get(k, None)
        except AttributeError:
            d[0] = dict([line.split() for line in dict_string.split('\n')])
            return d[0].get(k, None)

    return wrapper

query_e = query_wrapper_e()


def test(f):
    for k in 'ABCDEFG':
        f(k)


if __name__ == '__main__':
    print perf.perf(test, query)
    print perf.perf(test, query_e)
