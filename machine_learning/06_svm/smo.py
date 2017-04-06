#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: SVM 的一种实现，SMO（Sequential Minimal Optimization），二分类，类别标签使用-1和1，算法具有随机性
    @author: wujiabin@baidu.com
    @date: 06/04/2017
"""

import random
import numpy as np


def loadDataSet(fileName):
    """ 读取文件，返回数据集和标记数据
    """
    dataMat = []
    labelMat = []

    with open(fileName) as fr:
        for line in fr:
            lineAttr = line.strip().split('\t')
            dataMat.append([float(lineAttr[0]), float(lineAttr[1])])
            labelMat.append(float(lineAttr[2]))
    return dataMat, labelMat


def selectJrand(i, m):
    """ 随机选取一个在[0, m]范围内且不等于i的j 
    """
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j


def clipAlpha(aj, H, L):
    """ alpha 不可以大于H 或者 小于L，超过范围需要修正到范围内
    """
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj


def smoSimple(dataMatIn, classLabels, C, toler, maxIter, debug=False):
    """ 
    :param dataMatIn: 数据集
    :param classLabels: 标签
    :param C: 常数
    :param toler: 容错率
    :param maxIter: 最大循环次数
    :return: b, alphas
    """

    def log(msg):
        if debug:
            print msg

    dataMatrix = np.mat(dataMatIn)  # m X n
    labelMat = np.mat(classLabels).transpose()  # m X 1

    b = 0
    m, n = np.shape(dataMatrix)

    # 初始化 alpha 为 0
    alphas = np.mat(np.zeros((m, 1)))  # m X 1
    iter = 0

    def fError(dataMatrix, labelMat, alphas, b, i):
        """ 公式，用于计算误差 e
        """
        # m X 1 -> T -> 1 X m | m X n * n X 1 -> m X 1, 最终前面将变为一个 1 X 1 的矩阵，结果为一个数
        # 公式含义：w=∑αyx ?
        fx = float(np.multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
        e = fx - float(labelMat[i])
        return e

    while iter < maxIter:
        alphaPairsChanged = 0

        for i in range(m):

            Ei = fError(dataMatrix, labelMat, alphas, b, i)

            if (labelMat[i] * Ei < -toler and alphas[i] < C) or (labelMat[i] * Ei > toler and alphas[i] > 0):
                # 随机选取一行
                j = selectJrand(i, m)

                Ej = fError(dataMatrix, labelMat, alphas, b, j)

                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()

                if labelMat[i] != labelMat[j]:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])

                if L == H:
                    log('L == H; continue')
                    continue

                eta = float(2.0 * dataMatrix[i, :] * dataMatrix[j, :].T
                            - dataMatrix[i, :] * dataMatrix[i, :].T
                            - dataMatrix[j, :] * dataMatrix[j, :].T)

                if eta >= 0:
                    log('eta >= 0; continue')
                    continue

                alphas[j] -= float(labelMat[j] * (Ei - Ej) / eta)
                alphas[j] = clipAlpha(alphas[j], H, L)

                if abs(alphas[j] - alphaJold) < 0.00001:
                    log('j not moving enough')
                    continue

                # i 和 j 修改方向相反
                alphas[i] += float(labelMat[j] * labelMat[i] * (alphaJold - alphas[j]))

                b1 = float(b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T
                             - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T)

                b2 = float(b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T
                             - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T)

                if 0 < alphas[i] < C:
                    b = b1
                elif 0 < alphas[j] < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                alphaPairsChanged += 1
                log('iter: %d, i: %d, pairs changed %d.' % (iter, i, alphaPairsChanged))
        if alphaPairsChanged == 0:
            iter += 1
        else:
            iter = 0
        log('iteration number: %d' % iter)
    return b, alphas


# 完整 Platt SMO 算法

class PlattSMOImpl(object):

    def __init__(self, dataMatIn, classLabels, C, toler, maxIter, kTup=None, debug=False):
        self.X = np.mat(dataMatIn)
        self.labelMat = np.mat(classLabels).transpose()
        self.C = C
        self.toler = toler
        self.m, self.n = np.shape(dataMatIn)
        self.alphas = np.mat(np.zeros((self.m, 1)))
        self.b = 0
        # 误差缓存，第一列为 1，表示有缓存，否则为没有
        self.eCache = np.mat(np.zeros((self.m, 2)))
        self.maxIter = maxIter
        self.debug = debug
        self.kTup = kTup

        if kTup:
            self.K = np.mat(np.zeros((self.m, self.m)))
            for i in range(self.m):
                self.K[:, i] = self.kernelTrans(self.X, self.X[i, :])

    def kernelTrans(self, X, A):
        """ kernel 核函数，将数据映射到无穷维的空间，流行的径向基函数（radial bias function）"""
        m, n = np.shape(X)
        K = np.mat(np.zeros((m, 1)))
        if self.kTup[0] == 'lin':
            K = X * A.T
        elif self.kTup[0] == 'rbf':
            for j in range(m):
                deltaRow = X[j, :] - A
                K[j] = deltaRow * deltaRow.T
            K = np.exp(K / (-1 * self.kTup[1] ** 2))
        else:
            raise NameError('The kernel is not recognized.')
        return K

    def log(self, msg):
        if self.debug:
            print msg

    def calcEk(self, k):
        """ 计算误差 """
        if self.kTup:
            fXk = float(np.multiply(self.alphas, self.labelMat).T * self.K[:, k]) + self.b
        else:
            fXk = float(np.multiply(self.alphas, self.labelMat).T * (self.X * self.X[k, :].T)) + self.b
        Ek = fXk - float(self.labelMat[k])
        return Ek

    def selectJ(self, i, Ei):
        maxK = -1
        maxDeltaE = 0
        Ej = 0

        self.eCache[i] = [1, Ei]
        validEcacheList = np.nonzero(self.eCache[:, 0].A)[0]
        if validEcacheList.any():
            for k in validEcacheList:
                if k == i:
                    continue
                Ek = self.calcEk(k)
                deltaE = abs(Ei - Ek)
                if deltaE > maxDeltaE:
                    maxK = k
                    maxDeltaE = deltaE
                    Ej = Ek
            return maxK, Ej
        else:
            j = selectJrand(i, self.m)
            Ej = self.calcEk(j)
            return j, Ej

    def updateEk(self, k, Ek):
        self.eCache[k] = [1, Ek]

    def innerL(self, i):
        Ei = self.calcEk(i)

        if ((self.labelMat[i] * Ei < -self.toler and self.alphas[i] < self.C) or
                (self.labelMat[i] * Ei > self.toler and self.alphas[i] > 0)):
            j, Ej = self.selectJ(i, Ei)

            alphaIold = self.alphas[i].copy()
            alphaJold = self.alphas[j].copy()

            if self.labelMat[i] != self.labelMat[j]:
                L = max(0, self.alphas[j] - self.alphas[i])
                H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
            else:
                L = max(0, self.alphas[j] + self.alphas[i] - self.C)
                H = min(self.C, self.alphas[j] + self.alphas[i])

            if L == H:
                self.log('L == H')
                return 0

            if self.kTup:
                eta = float(2.0 * self.K[i, j] - self.K[i, i] - self.K[j, j])
            else:
                eta = float(2.0 * self.X[i, :] * self.X[j, :].T
                            - self.X[i, :] * self.X[i, :].T
                            - self.X[j, :] * self.X[j, :].T)

            if eta >= 0:
                self.log('eta >= 0')
                return 0

            self.alphas[j] -= float(self.labelMat[j] * (Ei - Ej) / eta)
            self.alphas[j] = clipAlpha(self.alphas[j], H, L)
            self.updateEk(j, Ej)

            if abs(self.alphas[j] - alphaJold) < 0.00001:
                self.log('j not moving enough')
                return 0

            self.alphas[i] += float(self.labelMat[j] * self.labelMat[i] * (alphaJold - self.alphas[j]))
            self.updateEk(i, Ei)

            if self.kTup:
                b1 = float(self.b - Ei - self.labelMat[i] * (self.alphas[i] - alphaIold) * self.K[i, i]
                           - self.labelMat[j] * (self.alphas[j] - alphaJold) * self.K[i, j])

                b2 = float(self.b - Ej - self.labelMat[i] * (self.alphas[i] - alphaIold) * self.K[i, j]
                           - self.labelMat[j] * (self.alphas[j] - alphaJold) * self.K[j, j])
            else:
                b1 = float(self.b - Ei - self.labelMat[i] * (self.alphas[i] - alphaIold) * self.X[i, :] * self.X[i, :].T
                           - self.labelMat[j] * (self.alphas[j] - alphaJold) * self.X[i, :] * self.X[j, :].T)

                b2 = float(self.b - Ej - self.labelMat[i] * (self.alphas[i] - alphaIold) * self.X[i, :] * self.X[j, :].T
                           - self.labelMat[j] * (self.alphas[j] - alphaJold) * self.X[j, :] * self.X[j, :].T)

            if 0 < self.alphas[i] < self.C:
                self.b = b1
            elif 0 < self.alphas[j] < self.C:
                self.b = b2
            else:
                self.b = (b1 + b2) / 2.0
            return 1
        else:
            return 0

    def smoP(self):
        iter = 0
        entireSet = True
        alphaPairsChanged = 0

        while iter < self.maxIter and (alphaPairsChanged > 0 or entireSet):
            alphaPairsChanged = 0
            iter += 1
            if entireSet:
                for i in range(self.m):
                    alphaPairsChanged += self.innerL(i)
                self.log('fullSet, iter: %d, i: %d, pairs changed %d' % (iter, i, alphaPairsChanged))
            else:
                nonBoundIs = np.nonzero((self.alphas.A > 0) * (self.alphas.A < self.C))[0]
                for i in nonBoundIs:
                    alphaPairsChanged += self.innerL(i)
                    self.log('non-bound, iter: %d, i: %d, pairs changed %d' % (iter, i, alphaPairsChanged))

            if entireSet:
                entireSet = False
            elif alphaPairsChanged == 0:
                entireSet = True

            self.log('iteration number: %d' % iter)
        return self.b, self.alphas


def calcWs(alphas, dataMatIn, classLabels):
    """ 计算 w: y = w.T * x + b
    """
    X = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()

    m, n = np.shape(X)

    w = np.zeros((n, 1))

    for i in range(m):
        w += np.multiply(alphas[i] * labelMat[i], X[i, :].T)
    return w


def classifySMO(data, ws, b):
    y = data * np.mat(ws) + b
    # y > 0, 1; y <= 0, -1
    return 1.0 if y > 0 else -1.0


def testRbf(k1=1.3):
    """ 测试RBF（径向基函数） """
    dataAttr, labelAttr = loadDataSet('testSetRBF.txt')

    smo = PlattSMOImpl(dataAttr, labelAttr, 200, 0.0001, 10000, ('rbf', k1))
    b, alphas = smo.smoP()

    dataMat = np.mat(dataAttr)
    labelMat = np.mat(labelAttr).transpose()

    # 支持向量
    SV_indexes = np.nonzero(alphas.A > 0)[0]
    SVs = dataMat[SV_indexes]
    SVlabels = labelMat[SV_indexes]

    print 'there are %d support vectors' % np.shape(SVs)[0]

    m, n = np.shape(dataMat)

    errorCount = 0
    for i in range(m):
        kernelEval = smo.kernelTrans(SVs, dataMat[i, :])
        predict = kernelEval.T * np.multiply(SVlabels, alphas[SV_indexes]) + b
        if np.sign(predict) != np.sign(labelAttr[i]):
            errorCount += 1

    print 'the training error rate is %f' % (1.0 * errorCount / m)

    dataAttr, labelAttr = loadDataSet('testSetRBF2.txt')
    dataMat = np.mat(dataAttr)
    labelMat = np.mat(labelAttr).transpose()
    m, n = np.shape(dataMat)
    errorCount = 0
    for i in range(m):
        kernelEval = smo.kernelTrans(SVs, dataMat[i, :])
        predict = kernelEval.T * np.multiply(SVlabels, alphas[SV_indexes]) + b
        if np.sign(predict) != np.sign(labelAttr[i]):
            errorCount += 1

    print 'the training error rate is %f' % (1.0 * errorCount / m)


if __name__ == '__main__':
    import time

    class Timer(object):

        def __enter__(self):
            self.start = time.time()
            print "#" * 120

        def __exit__(self, exc_type, exc_val, exc_tb):
            print '>>> elapsed time: {}'.format(time.time() - self.start)
            print "=" * 120

    with Timer():
        dataAttr, labelAttr = loadDataSet('testSet.txt')
        b, alphas = smoSimple(dataAttr, labelAttr, 0.6, 0.001, 40)
        print b, alphas[alphas > 0]
        print np.array(dataAttr)[np.nonzero(alphas)[0]], np.array(labelAttr)[np.nonzero(alphas)[0]]

        ws = calcWs(alphas, dataAttr, labelAttr)
        print ws

        dataMat = np.mat(dataAttr)
        print classifySMO(dataMat[2], np.mat(ws), b), labelAttr[2]

    with Timer():
        dataAttr, labelAttr = loadDataSet('testSet.txt')
        smo = PlattSMOImpl(dataAttr, labelAttr, 0.6, 0.001)
        b, alphas = smo.smoP(40)
        print b, alphas[alphas > 0]
        print np.array(dataAttr)[np.nonzero(alphas)[0]], np.array(labelAttr)[np.nonzero(alphas)[0]]

        ws = calcWs(alphas, dataAttr, labelAttr)
        print ws

        dataMat = np.mat(dataAttr)
        yi = dataMat[2] * np.mat(ws) + b
        print yi
        print classifySMO(dataMat[2], np.mat(ws), b), labelAttr[2]


    testRbf()
