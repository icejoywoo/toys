#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2018/10/16
"""

class Solution(object):

    def titleToNumber(self, s):
        """
        :type s: str
        :rtype: int
        """
        l = len(s)
        return sum([26 ** (l - i - 1) * (ord(c) - ord('A') + 1) for i, c in enumerate(s)])


if __name__ == '__main__':
    s = Solution()
    assert s.titleToNumber('A') == 1
    assert s.titleToNumber('B') == 2
    assert s.titleToNumber('AB') == 28
