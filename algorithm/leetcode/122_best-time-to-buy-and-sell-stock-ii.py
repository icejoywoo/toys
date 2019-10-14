#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
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
        for i, e in enumerate(prices):
            if e > buy:
                if e - buy > 0:
                    ret += e - buy
                    buy = e
            else:
                buy = e

        return ret


if __name__ == '__main__':
    s = Solution()
    assert s.maxProfit([]) == 0
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 7
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
