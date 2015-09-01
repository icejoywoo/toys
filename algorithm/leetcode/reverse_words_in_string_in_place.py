#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

class Solution:
    # @param s, a string
    # @return a string
    def reverseWords(self, s):

        # reverse whole string
        self.reverse(s, 0, len(s)-1)
        print s

        # reverse every word
        p = 0
        for i, e in enumerate(s):
            if e == ' ':
                self.reverse(s, p, i-1)
                p = i+1
        return s

    def reverse(self, s, p, q):
        # reverse whole string
        while p < q:
            s[p], s[q] = s[q], s[p]
            p += 1
            q -= 1


if __name__ == '__main__':
    s = Solution()
    # python不支持string assignments，伪代码无法运行
    print s.reverseWords("the sky is blue")
