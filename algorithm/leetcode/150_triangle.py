#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/triangle/
    @author: icejoywoo
    @date: 2019-10-12
"""

import collections


class Solution(object):

    def minimumTotalRecursive(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        l = len(triangle)
        ws = [len(i) for i in triangle]
        memo = {}

        def f(x, y):
            if (x, y) in memo:
                return memo[(x, y)]

            if x >= l or y >= ws[x]:
                memo[(x, y)] = 0
                return 0

            memo[(x, y)] = triangle[x][y] + min(f(x+1, y), f(x+1, y+1))
            return memo[(x, y)]

        return f(0, 0)

    def minimumTotalDP(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        l = len(triangle)

        dp = [[0] * (i+1) for i in range(l+1)]

        for i in range(l-1, -1, -1):
            for j, e in enumerate(triangle[i]):
                dp[i][j] = e + min(dp[i+1][j], dp[i+1][j+1])

        return dp[0][0]

    def minimumTotalDPCompress(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        l = len(triangle)

        # dp space only use one array
        dp = [0] * (l+1)

        for i in range(l-1, -1, -1):
            for j, e in enumerate(triangle[i]):
                dp[j] = e + min(dp[j], dp[j+1])

        return dp[0]

    def minimumTotalDP2(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        l = len(triangle)

        dp = collections.defaultdict(int)

        for i in range(l-1, -1, -1):
            for j, e in enumerate(triangle[i]):
                dp[i, j] = e + min(dp[i+1, j], dp[i+1, j+1])

        return dp[0, 0]

    minimumTotal = minimumTotalDPCompress


if __name__ == '__main__':
    s = Solution()
    assert s.minimumTotal([
         [2],
        [3,4],
       [6,5,7],
      [4,1,8,3]
    ]) == 11

    assert s.minimumTotal([[-1],[2,3],[1,-1,-3]]) == -1
