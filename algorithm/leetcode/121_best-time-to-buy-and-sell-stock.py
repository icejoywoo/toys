#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
    @author: icejoywoo
    @date: 2019-10-14
"""


class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        ret = 0
        buy = prices[0]
        buy_day = 0
        sell_day = None
        for i, e in enumerate(prices[1:], 1):
            if e > buy:
                profit = e - buy
                if profit > ret:
                    sell_day = i
                    ret = profit
            else:
                buy = e
                buy_day = i

        print buy_day+1, sell_day+1

        return ret


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([]) == 0
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
