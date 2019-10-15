#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
    @author: icejoywoo
    @date: 2019-10-15
"""


class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        l = len(prices)
        dp = [[[0, 0] for _ in range(2)] for _ in range(l)]
        dp[0] = [[0, -prices[0]], [0, -prices[0]]]
        res = 0

        for i in range(1, l):
            dp[i][0][0] = dp[i-1][1][1] + prices[i]  # 持有股票卖出，从11变为00

            dp[i][1][1] = max(dp[i-1][1][1], dp[i-1][1][0] - prices[i])

            dp[i][1][0] = max(dp[i-1][1][0], dp[i-1][0][0])

            res = max(dp[i][0][0], dp[i][0][1], dp[i][1][0], dp[i][1][1])

        print dp
        return res


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([1, 2, 4]) == 3
    assert s.maxProfit([1, 2, 3, 0, 2]) == 3
