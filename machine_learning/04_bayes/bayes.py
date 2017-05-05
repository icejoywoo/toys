#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 朴素贝叶斯
    @author: icejoywoo
    @date: 25/03/2017
"""

import numpy


def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    # 1 is abusive, 0 not
    return postingList,classVec


def createVocabList(dataSet):
    vocabSet = set()
    for document in dataSet:
        vocabSet |= set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word: %s is not in vocabulary.' % word
    return returnVec


listOfPosts, listClasses = loadDataSet()
myVocabList = createVocabList(listOfPosts)
print myVocabList


def trainNBOriginal(trainMatrix, trainCategory):
    """ 原始实现
    """
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])

    pAbusive = sum(trainCategory) * 1.0 / numTrainDocs # abusive prob

    # 向量：保存各个词出现的次数
    p0Num = numpy.zeros(numWords)
    p0Denom = 0.0

    p1Num = numpy.zeros(numWords)
    p1Denom = 0.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    # 频率向量，计算
    p1Vect = p1Num / p1Denom
    p0Vect = p0Num / p0Denom
    return p0Vect, p1Vect, pAbusive


def trainNB0(trainMatrix, trainCategory):
    """ 带有部分修正的实现
    """
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])

    pAbusive = sum(trainCategory) * 1.0 / numTrainDocs # abusive prob

    # 向量：保存各个词出现的次数，分母默认为2，分子默认为1，防止出现分母或分子为0的情况导致某一项为0
    p0Num = numpy.ones(numWords)
    p0Denom = 2.0

    p1Num = numpy.ones(numWords)
    p1Denom = 2.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    # 条件概率向量，计算
    p1Vect = numpy.log(p1Num / p1Denom)  # 为了防止下溢问题，加上了 ln
    p0Vect = numpy.log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive


listOfPosts, listClasses = loadDataSet()
trainMat = []
for postinDoc in listOfPosts:
    trainMat.append(setOfWords2Vec(myVocabList, postinDoc))

p0V, p1V, pAb = trainNB0(trainMat, listClasses)

print p0V, p1V, pAb


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + numpy.log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + numpy.log(1.0 - pClass1)
    return 1 if p1 > p0 else 0


def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print 'the word: %s is not in vocabulary.' % word
    return returnVec


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(numpy.array(trainMat), numpy.array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = numpy.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = numpy.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)


testingNB()
