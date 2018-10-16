#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2018/10/16
"""

parentheses = {
    "[": "]",
    "(": ")",
    "{": "}",
}

left_parentheses = parentheses.keys()
right_parentheses = parentheses.values()

class Solution(object):
    def __init__(self):
        self.stack = []

    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        for i in s:
            if i in left_parentheses:
                self.stack.append(i)
            elif i in right_parentheses:
                if self.stack:
                    left = self.stack.pop()
                    if i != parentheses[left]:
                        return False
                else:
                    return False

        if self.stack:
            return False
        else:
            return True

if __name__ == '__main__':
    s = Solution()
    assert s.isValid('()')
    assert s.isValid('()[]{}')
    assert s.isValid('([]){}')
    assert not s.isValid('(')
    assert not s.isValid('([]')
    assert not s.isValid('[(])')
    assert not s.isValid(')')
