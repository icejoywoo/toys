#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: a simple perf wrapper
    @author: icejoywoo
    @date: 15/12/6
"""

import time


def perf(func, *args, **kwargs):
    start = time.time()
    for _ in range(100000):
        func(*args, **kwargs)
    elapsed_time = time.time() - start
    return elapsed_time
