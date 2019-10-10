#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode-cn.com/problems/min-stack/
    @author: icejoywoo
    @date: 2019-10-10
"""


class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []  # list of (value, min_value)

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if self.stack:
            self.stack.append((x, min(self.stack[-1][1], x)))
        else:
            self.stack.append((x, x))

    def pop(self):
        """
        :rtype: None
        """
        self.stack.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1][0]

    def getMin(self):
        """
        :rtype: int
        """
        return self.stack[-1][1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()

if __name__ == '__main__':
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    assert minStack.getMin() == -3
    minStack.pop()
    assert minStack.top() == 0
    assert minStack.getMin() == -2
