#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {integer} x
    # @return {integer}
    def reverse(self, x):
        y = x
        result = 0
        while y:
            result = result * 10 + y % 10
            y /= 10

        # integer overflow [-2*31, 2*31-1]
        if result > 2147483647 or result < -2147483648:
            return 0
        else:
            return result


if __name__ == '__main__':
    assert Solution().reverse(-123) == -321