#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/climbing-stairs/
    和斐波那契数列一样
    @author: icejoywoo
    @date: 2019-10-11
"""


class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        dp = [0] * (n+1)

        dp[0] = 1
        dp[1] = 1

        for i in range(2, n+1):
            dp[i] = dp[i-1] + dp[i-2]

        return dp[n]


if __name__ == '__main__':
    s = Solution()
    assert s.climbStairs(2) == 2
    assert s.climbStairs(3) == 3