#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/26

import numpy
import os
import operator


def create_data_set():
    group = numpy.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dateSet, labels, k):
    dataSetSize = dateSet.shape[0]
    # 计算距离
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dateSet
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis=1)
    distances = sqDistance ** 0.5
    # argsort 返回索引值
    sortedDistIndices = distances.argsort()

    # 选取 k 个
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    # 排序获取最大的 label 为结果
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

group, labels = create_data_set()
assert classify0([0, 0], group, labels, 3) == 'B'


def file2matrix(filename):
    with open(filename) as fr:
        arrayOfLines = fr.readlines()

    numberOfLines = len(arrayOfLines)
    returnMat = numpy.zeros((numberOfLines, 3))

    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1

    return returnMat, classLabelVector


datingDateMat, datingLabels = file2matrix('datingTestSet2.txt')
assert classify0([10000, 2.326976, 1.953952], datingDateMat, datingLabels, 5) == 2


def autoNorm(dataSet):
    """
    """
    maxVals = dataSet.max(0)
    minVals = dataSet.min(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normDataSet = (dataSet - numpy.tile(minVals, (m, 1))) / numpy.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

# print autoNorm(datingDateMat)


def datingClassTest():
    hoRatio = 0.50      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount, numTestVecs


datingClassTest()


def img2vector(filename):
    """ 读取文件中的 0 和 1，转换为一个数组向量
    """
    returnMat = numpy.zeros((1, 1024))
    with open(filename) as fr:
        index = 0
        for line in fr:
            for i in range(32):
                returnMat[0, index*32+i] = int(line[i])
            index += 1
    return returnMat

def img2vector1(filename):
    returnVect = numpy.zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


print img2vector('trainingDigits/0_0.txt')


def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = numpy.zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))


handwritingClassTest()
