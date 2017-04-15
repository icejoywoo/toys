#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 机器学习实战 决策树
    @author: wujiabin@baidu.com
    @date: 25/03/2017
"""

import collections
import math
import operator


def calcShannonEnt(dataSet):
    """ 计算熵（entropy），也叫香农熵（shannon entropy）
    """
    # 样本总数
    numEntries = len(dataSet)
    # 标注结果计数
    labelCounts = collections.defaultdict(int)
    for featVec in dataSet:
        # 最后一位是标注结果
        currentLabel = featVec[-1]
        labelCounts[currentLabel] += 1

    # 熵计算公式
    shannonEnt = 0.0
    for label, count in labelCounts.iteritems():
        prob = float(count) / numEntries
        # 标记 label 的信息定义，熵是其累加和的负数
        shannonEnt -= prob * math.log(prob, 2)
    return shannonEnt


def createDataSet():
    """ 数据每一列都是一个 axis，对应一个坐标轴，每一行数据是一个向量
    :return:
    """
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no'],
    ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


dataSet, labels = createDataSet()

print calcShannonEnt(dataSet)

dataSet[0][-1] = 'maybe'

print calcShannonEnt(dataSet)


def splitDataSet(dataSet, axis, value):
    """ 按照给定的特征划分数据集，指定某一列数据为某个值
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            # 移除选取的某一列
            retDataSet.append(featVec[:axis] + featVec[axis+1:])
    return retDataSet


dataSet, labels = createDataSet()
print splitDataSet(dataSet, 0, 1)
print splitDataSet(dataSet, 0, 0)


def chooseBestFeatureToSplit(dataSet):
    """ 选择最好的数据集划分方式：就是熵最小，信息增益最大
    信息增益：原始的熵 - 切分数据集后的熵，就是切分数据集后的熵最小
    """
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)

    bestInfoGain = 0.0
    bestFeature = None

    for i in range(numFeatures):
        uniqValues = {example[i] for example in dataSet}
        newEntropy = 0.0

        for value in uniqValues:
            subDataSet = splitDataSet(dataSet, i, value)
            # 划分的数据集的概率
            prob = len(subDataSet) * 1.0 / len(dataSet)
            # 子集概率 * 子集的熵 是 新熵的一部分
            newEntropy += prob * calcShannonEnt(subDataSet)

        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


print chooseBestFeatureToSplit(dataSet)


def majorityCnt(classList):
    """ 获取标签数最多的数量
    """
    classCount = collections.defaultdict(int)
    for vote in classList:
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    """ 决策树模型结果，可以序列化存储起来供后续使用
    """
    classList = [example[-1] for example in dataSet]

    # 递归终止条件
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    bestFeature = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]

    myTree = {
        bestFeatureLabel: {}
    }

    uniqValues = {example[bestFeature] for example in dataSet}
    for value in uniqValues:
        # list copy
        subLabels = labels[:bestFeature] + labels[bestFeature+1:]
        myTree[bestFeatureLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLabels)

    return myTree

myTree = createTree(dataSet, labels)


def classify(inputTree, featLabels, testVec):
    firstLabel = inputTree.iterkeys().next()
    secondDict = inputTree[firstLabel]
    featIndex = featLabels.index(firstLabel)

    for key, value in secondDict.iteritems():
        if testVec[featIndex] == key:
            if isinstance(value, dict):
                classLabel = classify(value, featLabels, testVec)
            else:
                classLabel = value

    return classLabel


print classify(myTree, labels, [1, 0])
print classify(myTree, labels, [1, 1])
