#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/decode-ways/
    @author: icejoywoo
    @date: 2019-10-11
"""

import string

mapping = dict(zip(list(string.ascii_uppercase), range(1, 27)))
rmapping = dict(zip(range(1, 27), list(string.ascii_uppercase)))


class Solution(object):
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """

        cache = {}

        def f(sub):
            if not sub:
                return 1

            if int(sub[0]) in rmapping:
                if sub[1:] in cache:
                    print "bingo", sub[1:], cache[sub[1:]]
                    r1 = cache[sub[1:]]
                else:
                    r1 = f(sub[1:])
                    cache[sub[1:]] = r1

                r2 = 0
                if len(sub) >= 2 and int(sub[0:2]) in rmapping:
                    if sub[2:] in cache:
                        print "bingo:", sub[2:], cache[sub[2:]]
                        r2 = cache[sub[2:]]
                    else:
                        r2 = f(sub[2:])
                        cache[sub[2:]] = r2
                return r1 + r2
            else:
                return 0

        return f(s)


if __name__ == '__main__':
    s = Solution()
    assert s.numDecodings('0') == 0
    assert s.numDecodings('01') == 0
    assert s.numDecodings('12') == 2
    assert s.numDecodings('226') == 3
    print s.numDecodings("9371597631128776948387197132267188677349946742344217846154932859125134924241649584251978418763151253")
