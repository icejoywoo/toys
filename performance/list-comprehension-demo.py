#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 15/12/6
"""

import perf


def even_filter_lc():
    """ list comprehension
    """
    return [i for i in xrange(1000) if i % 2 == 0]


def even_filter():
    r = []
    for i in xrange(1000):
        if i % 2 == 0:
            r.append(i)
    return r


if __name__ == '__main__':
    print perf.perf(even_filter)
    print perf.perf(even_filter_lc)