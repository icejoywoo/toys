#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {string[]} strs
    # @return {string}
    def longestCommonPrefix(self, strs):
        """ 不考虑None的情况
        :param strs:
        :return:
        """
        prefix = []
        for chars in zip(*strs):
            if len(set(chars)) == 1:
                prefix.append(chars[0])
            else:
                break
        return ''.join(prefix)


if __name__ == '__main__':
    s = Solution()
    assert s.longestCommonPrefix(['a', 'ab', 'abc']) == 'a'
    assert s.longestCommonPrefix(['', 'ab', 'abc']) == ''
    assert s.longestCommonPrefix([None, 'ab', 'abc']) == ''
    assert s.longestCommonPrefix([]) == ''
    assert s.longestCommonPrefix(["aca","cba"]) == ''
