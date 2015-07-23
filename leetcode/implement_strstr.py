#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {string} haystack
    # @param {string} needle
    # @return {integer}
    def strStr(self, haystack, needle):

        if len(needle) > len(haystack):
            return -1

        i = j = 0
        l = 0
        while i + l < len(haystack) and j < len(needle):
            if haystack[i+l] == needle[j]:
                l += 1
                j += 1
            else:
                i += max(l, 1)
                l = 0
                j = 0
        if haystack[i:i+l] == needle:
            return i
        else:
            return -1


if __name__ == '__main__':
    s = Solution()
    assert s.strStr('abcd', 'bc') == 1
    assert s.strStr('aaa', 'aaaa') == -1
    assert s.strStr('', '') == 0
    assert s.strStr('a', 'b') == -1
    assert s.strStr('a', 'a') == 0
    assert s.strStr("mississippi", "issipi") == -1
