#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/27

__author__ = 'icejoywoo'


import numpy as np

# create a 3D numpy array
arr = np.zeros((3, 3, 3))


a = np.array([
    [11, 12, 13],
    [21, 22, 23],
    [31, 32, 33],
])
print a.T
# 多维数据用 , 分割，表示对不同维度的操作
print a[1,:]

print np.nonzero(a[:,0])[0]

print np.eye(5)

print np.linalg.det(a)  # det == 0.0 说明矩阵不可逆

print np.nonzero(a[a == 22])
print np.nonzero(a)
print np.nonzero(a > 22)

print np.nonzero(a.reshape(1, 9))
