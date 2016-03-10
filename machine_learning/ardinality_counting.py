#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 16/2/18
"""

from numpy.random import uniform

a = [uniform(0, 1) for _ in xrange(10000000)]

_min = min(a)

print 1 / _min