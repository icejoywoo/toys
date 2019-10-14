#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
    @author: icejoywoo
    @date: 2019/10/14
"""


class Solution(object):
    def maxProfitDP(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        l = len(prices)
        dp = [[[0, 0] for _ in range(k+1)] for _ in range(l+1)]
        dp[0] = [[0, -prices[0]] for _ in range(k+1)]
        res = 0

        for i in range(1, l):
            for j in range(k):
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i-1][j+1][0] - prices[i], dp[i-1][j][1])
                res = max(res, dp[i][j][0], dp[i][j][1])

        return res

    def maxProfit(self, k, prices):
        """
        需要状态压缩，不知道如何压缩
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        l = len(prices)
        dp = [[[0, 0] for _ in range(2)] for _ in range(2)]
        dp[0] = [[0, -prices[0]] for _ in range(2)]
        res = 0

        for i in range(1, l):
            for j in range(k):
                x, x0 = i % 2, (i-1) % 2
                y, y1 = j % 2, (j+1) % 2
                dp[x][y][0] = max(dp[x0][y][0], dp[x0][y][1] + prices[i])
                dp[x][y][1] = max(dp[x0][y1][0] - prices[i], dp[x0][y][1])
                res = max(res, dp[x][y][0], dp[x][y][1])

        return res


if __name__ == '__main__':
    s = Solution()
    print s.maxProfit(2, [3, 3, 5, 0, 0, 3, 1, 4])
    assert s.maxProfit(2, [2, 4, 1]) == 2
    assert s.maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7
    assert s.maxProfit(2, [3, 3, 5, 0, 0, 3, 1, 4]) == 6
