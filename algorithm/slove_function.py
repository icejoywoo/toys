#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: http://www.keakon.net/2011/05/08/3行Python代码解简单的一元一次方程
    @author: icejoywoo
    @date: 15/12/1
"""

from __future__ import division


def solve(f, var='x'):
    f = f.replace("=", "-(")+")"
    c = eval(f, {var: 1j})
    print c
    return -c.real/c.imag


if __name__ == '__main__':
    print solve("x - 2*x + 5*x - 46*(235-24) = x + 2")
    print solve("x = 5")
