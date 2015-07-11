#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {integer} x
    # @return {integer}
    def reverse(self, x):
        s = str(x)
        # 是否带有负号
        if s[0] == '-':
            result = int('-%s' % s[1:][::-1])
        else:
            result = int(s[::-1])

        if result > 2**31 - 1 or result < -2**31:
            return 0
        else:
            return result


if __name__ == '__main__':
    print Solution().reverse(-123) == -321