#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/coin-change/
    @author: icejoywoo
    @date: 2019-10-15
"""


class Solution(object):
    def coinChange(self, coins, amount):
        """
        :type coins: List[int]
        :type amount: int
        :rtype: int
        """
        default_value = amount + 1
        dp = [default_value for _ in range(amount+1)]
        dp[0] = 0
        coins.sort()

        for i in range(amount+1):
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], dp[i-coin] + 1)

        return -1 if dp[amount] > amount else dp[amount]


if __name__ == '__main__':
    s = Solution()
    assert s.coinChange([1, 2, 5], 11) == 3
    assert s.coinChange([2], 3) == -1
    assert s.coinChange([1, 6, 7], 30) == 5
