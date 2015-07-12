#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {integer} x
    # @return {boolean}
    def isPalindrome(self, x):
        if x < 0:
            return False
        y = x
        div = 1
        while y / div >= 10:
            div *= 10

        while y:
            print y, div
            l = y / div
            r = y % 10
            if l != r:
                return False
            y = (y % div) / 10
            div /= 100
        return True


if __name__ == '__main__':
    assert Solution().isPalindrome(121) == True
    assert Solution().isPalindrome(1001) == True
    assert Solution().isPalindrome(-121) == False
