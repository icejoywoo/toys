#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
    @author: icejoywoo
    @date: 2019-10-15
"""


class Solution(object):
    def maxProfit(self, prices, fee):
        """
        :type prices: List[int]
        :type fee: int
        :rtype: int
        """
        if not prices:
            return 0

        l = len(prices)
        dp = [[0, 0] for _ in range(2)]
        dp[0] = [0, -prices[0] - fee]
        res = 0

        for i in range(1, l):
            x, x0 = i % 2, (i-1) % 2
            dp[x][0] = max(dp[x0][0], dp[x0][1] + prices[i])
            dp[x][1] = max(dp[x0][1], dp[x0][0] - prices[i] - fee)
            res = max(dp[x][0], dp[x][1])

        return res


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([1, 3, 2, 8, 4, 9], 2) == 8
