#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/
    @author: icejoywoo
    @date: 2019-10-14
"""


class Solution(object):
    def maxProfitBF(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        l = len(prices)

        def f(start, hasStock, count, profit):
            # last one
            if start == l - 1:
                return profit + prices[start] if hasStock else profit

            if hasStock:
                return max(f(start + 1, True, count, profit),
                           f(start + 1, False, count, profit + prices[start]))
            elif count > 0 and not hasStock:
                return max(f(start + 1, False, count, profit),
                           f(start + 1, True, count - 1, profit - prices[start]))
            else:
                return f(start + 1, hasStock, count, profit)

        if prices:
            return f(0, False, 2, 0)
        else:
            return 0

    def maxProfitDP(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0
        l = len(prices)
        dp = [[[0, 0] for _ in range(3)] for _ in range(l)]
        dp[0] = [[0, -prices[0]] for _ in range(3)]

        for i in range(1, l):
            for j in range(2):
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j+1][0] - prices[i])

        return max([dp[l-1][i][0] for i in range(3)])

    maxProfit = maxProfitDP


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([]) == 0
    assert s.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]) == 6
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
