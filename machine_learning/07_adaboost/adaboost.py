#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: adaboost(adaptive boosting)
    @author: icejoywoo
    @date: 28/03/2017
"""

import numpy as np


def loadSimpleData():
    dataMat = np.matrix([
        [1., 2.1],
        [2., 1.1],
        [1.3, 1.],
        [1., 1.],
        [2., 1.],
    ])
    labels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataMat, labels


def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
    """
    :param dataMatrix: 输入数据
    :param dimen: 列维度
    :param threshVal: 阈值，临界值
    :param threshIneq: 操作，'lt' 'gt'
    :return: 预测分类结果
    """
    retArray = np.ones((np.shape(dataMatrix)[0], 1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:, dimen] > threshVal] = -1.0
    return retArray


def buildStump(dataAttr, classLabels, D):
    dataMatrix = np.mat(dataAttr)
    labelMat = np.mat(classLabels).T

    m, n = np.shape(dataMatrix)
    numSteps = 10

    bestStump = {}
    bestClasEst = np.mat(np.zeros((m, 1)))

    minError = np.inf

    for i in range(n):
        rangeMin = dataMatrix[:, i].min()
        rangeMax = dataMatrix[:, i].max()
        stepSize = (rangeMax - rangeMin) * 1.0 / numSteps

        for j in range(-1, numSteps + 1):
            for inequal in ('lt', 'gt'):
                threshVal = rangeMin + j * stepSize
                predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)

                # errArr 1 表示数据错误，0表示数据预测正确
                errArr = np.mat(np.ones((m, 1)))
                errArr[predictedVals == labelMat] = 0

                weightedError = D.T * errArr # 矩阵：1 X m，m X 1 最后得出一个数
                # print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump = {
                        'dim': i,
                        'thresh': threshVal,
                        'ineq': inequal,
                    }
        return bestStump, minError, bestClasEst


def adaBoostTrainDS(dataAttr, classLabels, numIt=40):
    """
    :param dataAttr: 输入数据
    :param classLabels: 标记结果
    :param numIt: 最大迭代次数
    :return: 弱分类器的列表
    """
    weakClassArr = []

    m, n = np.shape(dataAttr)
    D = np.mat(np.ones((m, 1)) / m)

    # 估计累计值
    aggClassEst = np.mat(np.zeros((m, 1)))

    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataAttr, classLabels, D)

        print 'D:', D.T

        # 分类器权重值 alpha
        alpha = float(0.5 * np.log((1.0 - error) / max(error, 1e-16)))

        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print 'classEst:', classEst.T

        # 更新 D
        expon = np.multiply(-1 * alpha * np.mat(classLabels).T, classEst)
        D = np.multiply(D, np.exp(expon))
        D = D / D.sum()

        aggClassEst += alpha * classEst
        print 'aggClassEst:', aggClassEst

        aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T, np.ones((m, 1)))
        errorRate = aggErrors.sum() / m

        print 'total error:', errorRate, '\n'
        if errorRate == 0.0:
            break
    return weakClassArr


def adaClassify(dataToClass, classifierArr):
    dataMatrix = np.mat(dataToClass)
    m, n = np.shape(dataMatrix)
    aggClassEst = np.mat(np.zeros((m, 1)))

    for i, c in enumerate(classifierArr):
        classEst = stumpClassify(dataMatrix, c['dim'], c['thresh'], c['ineq'])
        aggClassEst += c['alpha'] * classEst
        print aggClassEst
    return np.sign(aggClassEst)

dataMat, labels = loadSimpleData()
D = np.mat(np.ones((5, 1)) / 5)
print buildStump(dataMat, labels, D)
classifierArr = adaBoostTrainDS(dataMat, labels, 9)

print adaClassify([[5, 5], [0,0]], classifierArr)
