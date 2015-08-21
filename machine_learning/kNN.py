#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/26

__author__ = 'wujiabin'

from numpy import *
import operator


def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

print create_data_set()

