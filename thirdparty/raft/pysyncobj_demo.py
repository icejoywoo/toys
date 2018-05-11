#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: pysyncobj raft demo
    @author: icejoywoo
    @date: 24/02/2018
"""

from pysyncobj import SyncObj, replicated
from pysyncobj.batteries import ReplCounter, ReplDict

counter1 = ReplCounter()
counter2 = ReplCounter()
dict1 = ReplDict()
# 构造函数会默认启动服务，根据第一个参数的endpoint来启动服务，用于通信
syncObj = SyncObj('localhost:4321', [], consumers=[counter1, counter2, dict1])

counter1.set(42, sync=True)  # set initial value to 42, 'sync' means that operation is blocking
counter1.add(10, sync=True)  # add 10 to counter value
counter2.inc(sync=True)  # increment counter value by one
dict1.set('testKey1', 'testValue1', sync=True)
dict1['testKey2'] = 'testValue2'  # this is basically the same as previous, but asynchronous (non-blocking)
print(counter1, counter2, dict1['testKey1'], dict1.get('testKey2'))


class MyCounter(SyncObj):
    def __init__(self):
        super(MyCounter, self).__init__('localhost:4321', [])
        self.__counter = 0

    @replicated
    def inc_counter(self):
        self.__counter += 1

    def get_counter(self):
        return self.__counter
