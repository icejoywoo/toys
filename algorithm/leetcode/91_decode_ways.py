#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/decode-ways/
    @author: icejoywoo
    @date: 2019-10-11
"""

import string

mapping = dict(zip(list(string.ascii_uppercase), range(1, 27)))
rmapping = {str(k): v for k, v in dict(zip(range(1, 27), list(string.ascii_uppercase))).items()}


class Solution(object):
    def numDecodingsRecursive(self, s):
        """
        :type s: str
        :rtype: int
        """

        cache = {}

        def f(sub):
            # sub is empty means done
            if not sub:
                return 1

            if sub[0] in rmapping:
                if sub[1:] in cache:
                    print "bingo", sub[1:], cache[sub[1:]]
                    r1 = cache[sub[1:]]
                else:
                    r1 = f(sub[1:])
                    cache[sub[1:]] = r1

                r2 = 0
                if len(sub) >= 2 and sub[0:2] in rmapping:
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

    def numDecodingsIter(self, s):
        """
        递归公式参考： https://leetcode.com/problems/decode-ways/discuss/401834/Simple-C%2B%2B-DP
        :type s: str
        :rtype: int
        """

        l = len(s)
        dp = [0] * (l+1)
        dp[0] = 1
        dp[1] = 1 if s[0] in rmapping else 0

        for i in range(2, l+1):
            r1 = dp[i-1] if s[i-1] in rmapping else 0
            r2 = dp[i-2] if s[i-2:i] in rmapping else 0
            dp[i] = r1 + r2

        return dp[l]

    numDecodings = numDecodingsIter


if __name__ == '__main__':
    s = Solution()
    assert s.numDecodings('0') == 0
    assert s.numDecodings('01') == 0
    assert s.numDecodings('10') == 1
    assert s.numDecodings('12') == 2
    assert s.numDecodings('226') == 3
    assert s.numDecodings("9371597631128776948387197132267188677349946742344217846154932859125134924241649584251978418763151253") == 3981312
