#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 逻辑回归
    @author: icejoywoo
    @date: 26/03/2017
"""
import numpy
import random


def loadDataSet():
    dataMat = []
    labelMat = []
    with open('testSet.txt') as fr:
        for line in fr:
            lineAttr = line.strip().split()
            # x0, x1, x2 其中 x0 为缺失数据，直接设置为 1
            dataMat.append([1.0, float(lineAttr[0]), float(lineAttr[1])])
            labelMat.append(int(lineAttr[2]))
    return dataMat, labelMat


def sigmoid(inX):
    """ sigmoid 函数: 1 / (1 + e^-z), z = w0x0 + w1x1 + ... + wnxn = w^T * x (矩阵乘法，T表示转置）
    """
    return 1.0 / (1 + numpy.exp(-inX))


def gradAscent(dataMat, classLabels):
    """ 梯度上升（与梯度下降对应，weights 更新函数变为 减号 即可
    """
    dataMatrix = numpy.mat(dataMat)
    labelMat = numpy.mat(classLabels).transpose()  # 转置
    m, n = dataMatrix.shape
    alpha = 0.001
    maxCycles = 500
    # w 矩阵，直接初始化为 n 行 1 列的矩阵，无需转置
    weights = numpy.ones((n, 1))

    for k in range(maxCycles):
        # z = w0x0 + w1x1 + ... + wnxn = w^T * x (矩阵乘法，T表示转置）
        h = sigmoid(dataMatrix * weights)
        # 函数计算的错误矩阵：标记结果 - 函数计算结果
        error = labelMat - h
        weights += alpha * dataMatrix.transpose() * error
    return weights


dataMat, labelMat = loadDataSet()

print gradAscent(dataMat, labelMat)


def stocGradAscent0(dataMat, classLabels):
    """ 随机梯度上升，快速收敛
    """
    dataMatrix = numpy.array(dataMat)
    m, n = dataMatrix.shape
    alpha = 0.01
    weights = numpy.ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights += dataMatrix[i] * alpha * error
    return weights


dataMat, labelMat = loadDataSet()
print stocGradAscent0(dataMat, labelMat)


def stocGradAscent1(dataMat, classLabels, numIter=150):
    """ 随机梯度上升改进
    """
    dataMatrix = numpy.array(dataMat)
    m, n = dataMatrix.shape
    weights = numpy.ones(n)

    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4 / (1.0 + i + j) + 0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights += dataMatrix[randIndex] * alpha * error
            del dataIndex[randIndex]

    return weights

dataMat, labelMat = loadDataSet()
print stocGradAscent1(dataMat, labelMat, 500)


def classifyVector(inX, weights):
    """
    """
    prob = sigmoid(sum(inX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


dataMat, labelMat = loadDataSet()
weights = stocGradAscent1(dataMat, labelMat, 500)
assert classifyVector(numpy.array([1.0, 0.677983, 2.556666]), weights) == 1
assert classifyVector(numpy.array([1.0, 0.761349, 10.693862]), weights) == 0
assert classifyVector(numpy.array([1.0, -2.168791, 0.143632]), weights) == 1
assert classifyVector(numpy.array([1.0, 1.388610, 9.341997]), weights) == 0
assert classifyVector(numpy.array([1.0, 0.317029, 14.739025]), weights) == 0
