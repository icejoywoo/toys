#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/edit-distance/
    @author: icejoywoo
    @date: 2019-09-24
"""

# DP
class Solution(object):
    def minDistance(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """
        m, n = len(word1), len(word2)
        dp = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]

        for i in xrange(m + 1):
            dp[i][0] = i

        for j in xrange(n + 1):
            dp[0][j] = j

        for i in xrange(1, m+1):
            for j in xrange(1, n+1):
                dp[i][j] = min(
                    dp[i-1][j-1] + (0 if word1[i-1] == word2[j-1] else 1),
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1
                )

        return dp[m][n]


if __name__ == '__main__':
    s = Solution()
    assert s.minDistance("horse", "ros") == 3
