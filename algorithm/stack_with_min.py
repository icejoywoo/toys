#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

"""
实现一个栈，满足min() pop() push()方法的时间复杂度都为O(1).(min()返回栈中最小元素)

思路：把data和最小值看作整体作为一个element，作为stack的element
"""

class Stack(object):

    def __init__(self):
        self._stack = []
        self._min = None

    def push(self, element):
        if self._min and element < self._min:
            self._min = element
        elif self._min is None:
            self._min = element
        self._stack.append((element, self._min))

    def pop(self):
        last, _ = self._stack.pop()
        if self._stack:
            self._min = self._stack[-1][1]
        else:
            self._min = None
        return last

    def min(self):
        return self._min

    def __len__(self):
        return len(self._stack)


if __name__ == '__main__':

    s = Stack()

    assert s.min() is None

    s.push(3)
    assert s.min() == 3
    s.push(4)
    assert s.min() == 3
    s.push(5)
    assert s.min() == 3

    s.push(1)
    assert s.min() == 1

    s.pop()
    assert s.min() == 3

    s.pop()
    s.pop()
    s.pop()
    assert s.min() is None
