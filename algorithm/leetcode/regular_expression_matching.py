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

        # pattern字符串已经消耗完毕
        if p_len == 0:
            return s_len == 0

        # 仅剩一个字符的情况
        if p_len == 1:
            if s_len == 1:
                return s[i] == p[j] or p[j] == '.'
            else:
                return False

        if p[i+1] == '*':
            while i < s_len and j < p_len and (s[i] == p[j] or p[j] == '.'):
                if self.isMatch(s[i:], p[j+2:]):
                    return True
                i += 1
            return self.isMatch(s[i:], p[j+2:])
        else:
            if i < s_len and j < p_len:
                return (s[i] == p[j] or p[i] == '.') and self.isMatch(s[i+1:], p[j+1:])
            else:
                return False


if __name__ == '__main__':
    assert Solution().isMatch('aa', 'a.')
    assert Solution().isMatch('aa', 'a') == False
    assert Solution().isMatch("aa", "a*")
    assert Solution().isMatch("aa", ".*")
    assert Solution().isMatch("ab", ".*")
    assert Solution().isMatch("aab", "c*a*b")
    assert Solution().isMatch("ab", ".*c") == False
    assert Solution().isMatch("a", ".*..a*") == False
    assert Solution().isMatch("aaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*c") == False