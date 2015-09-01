#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {string} s
    # @param {string} p
    # @return {boolean}
    def isMatch(self, s, p):
        s_len = len(s)
        p_len = len(p)
        i = j = 0
        last_char_in_p = p[0]
        while i < s_len and j < p_len:
            print i, j
            if p[j] == '.':
                last_char_in_p = p[j]
                i += 1
                j += 1
            elif p[j] == '*':
                if last_char_in_p == '.':
                    # .* 贪婪匹配
                    i += 1
                elif s[i] == last_char_in_p:
                    i += 1
                elif s[i] != last_char_in_p:
                    j += 1
            elif s[i] == p[j]:
                i += 1
                j += 1
            elif s[i] != p[j]:
                return False
        return True


if __name__ == '__main__':
    assert Solution().isMatch('aa', 'a.')
    assert Solution().isMatch('aa', 'a')