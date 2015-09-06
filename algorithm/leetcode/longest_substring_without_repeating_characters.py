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
        i = 0
        length = len(s)
        max_length = 0
        appered_before = set()

        start = 0

        while i < length:
            if s[i] not in appered_before:
                appered_before.add(s[i])
                i += 1
            else:
                max_length = max(i - start, max_length)
                new_start = s.find(s[i], start) + 1
                for j in xrange(start, new_start):
                    appered_before.remove(s[j])
                start = new_start

        max_length = max(i - start, max_length)

        return max_length


if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLongestSubstring('') == 0
    assert s.lengthOfLongestSubstring('c') == 1
    assert s.lengthOfLongestSubstring('bbbb') == 1
    assert s.lengthOfLongestSubstring('abcabcbb') == 3