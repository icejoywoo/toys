#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
    @author: icejoywoo
    @date: 2019/10/14
"""


class Solution(object):
    def maxProfit(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        l = len(prices)

        # 交易次数超过数组的一半说明可以直接贪婪交易了
        if k > l/2:
            return self.maxProfitGreedy(prices)

        dp = [[[0, 0] for _ in range(k+1)] for _ in range(2)]
        dp[0] = [[0, -prices[0]] for _ in range(k+1)]

        for i in range(1, l):
            for j in range(k):
                x, x0 = i % 2, (i - 1) % 2
                dp[x][j][0] = max(dp[x0][j][0], dp[x0][j][1] + prices[i])
                dp[x][j][1] = max(dp[x0][j+1][0] - prices[i], dp[x0][j][1])

        res = [dp[(l-1) % 2][i][0] for i in range(k)]
        if res:
            return max(res)
        else:
            return 0

    def maxProfitGreedy(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        res = 0
        l = len(prices)
        for i in range(1, l):
            if prices[i] > prices[i-1]:
                res += prices[i] - prices[i-1]

        return res


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit(2, [2, 4, 1]) == 2
    assert s.maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7
    assert s.maxProfit(2, [3, 3, 5, 0, 0, 3, 1, 4]) == 6
