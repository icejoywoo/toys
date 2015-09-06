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
        result = None
        appered_before = set()

        start = 0

        while i < length:
            if s[i] not in appered_before:
                appered_before.add(s[i])
                i += 1
            else:
                new_result = s[start:i]
                if result and len(result) < len(new_result):
                    result = new_result
                elif result is None:
                    result = new_result
                new_start = s.find(s[i], start) + 1
                for j in xrange(start, new_start):
                    appered_before.remove(s[j])
                start = new_start

        new_result = s[start:i]
        if result and len(result) < len(new_result):
            result = new_result
        elif result is None:
            result = new_result

        return len(result) if result else 0


if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLongestSubstring('') == 0
    assert s.lengthOfLongestSubstring('c') == 1
    assert s.lengthOfLongestSubstring('bbbb') == 1
    assert s.lengthOfLongestSubstring('abcabcbb') == 3