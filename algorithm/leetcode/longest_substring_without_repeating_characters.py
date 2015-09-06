#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/9/6

__author__ = 'wujiabin'


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        start = 0
        index = 0
        length = len(s)
        exist = set()
        max_len = 0

        while index < length:
            while s[index] in exist:
                exist.remove(s[start])
                start += 1

            exist.add(s[index])
            max_len = max(max_len, index - start + 1)
            index += 1

        return max_len


if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLongestSubstring('') == 0
    assert s.lengthOfLongestSubstring('c') == 1
    assert s.lengthOfLongestSubstring('bbbb') == 1
    assert s.lengthOfLongestSubstring('abcabcbb') == 3