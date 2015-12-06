#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 15/12/6
"""

import perf


if __name__ == '__main__':
    print perf.perf(range, 10000)
    print perf.perf(xrange, 10000)
