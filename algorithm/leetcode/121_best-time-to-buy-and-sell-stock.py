#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
    @author: icejoywoo
    @date: 2019-10-14
"""
import sys


class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        ret = 0
        buy = sys.maxint
        buy_day = sell_day = None

        for i, e in enumerate(prices):
            if e > buy:
                profit = e - buy
                if profit > ret:
                    sell_day = i + 1
                    ret = profit
            else:
                buy = e
                buy_day = i + 1

        if buy_day and sell_day:
            print buy_day, sell_day

        return ret


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([]) == 0
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
