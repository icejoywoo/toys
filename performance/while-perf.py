#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 15/12/6
"""

import dis

import perf


def while_true():
    while True:
        break


def while_1():
    while 1:
        break


if __name__ == '__main__':
    print perf.perf(while_true)
    print perf.perf(while_1)

    print dis.dis(while_true)
    print dis.dis(while_1)