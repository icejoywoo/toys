#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: wujiabin@baidu.com
    @date: 27/03/2017
"""

import time
import numpy as np
import svmMLiA

dataAttr, labelAttr = svmMLiA.loadDataSet('testSet.txt')

# 取值为 -1 和 1，与logistic回归不同
print labelAttr

start = time.time()
b, alphas = svmMLiA.smoSimple(dataAttr, labelAttr, C=0.6, toler=0.001, maxIter=40)
print "smoSimple elapsed: ", time.time() - start

print b, alphas[alphas > 0]

print np.shape(alphas[alphas > 0])

for i in range(100):
    if alphas[i] > 0:
        print alphas[i], labelAttr[i]


dataAttr, labelAttr = svmMLiA.loadDataSet('testSet.txt')

start = time.time()
b, alphas = svmMLiA.smoP(dataAttr, labelAttr, 0.6, 0.001, 40)
print "smoP elapsed: ", time.time() - start

