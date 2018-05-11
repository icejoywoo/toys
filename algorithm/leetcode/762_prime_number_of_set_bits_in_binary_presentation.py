#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/description/
    @author: icejoywoo
    @date: 2018/5/11
"""


class Solution(object):
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71)

    def countPrimeSetBits(self, L, R):
        """
        :type L: int
        :type R: int
        :rtype: int
        """
        ret = 0
        for i in range(L, R + 1):
            num_set_bits = bin(i).count('1')
            if num_set_bits in Solution.primes:
                ret += 1
        return ret


if __name__ == '__main__':
    s = Solution()
    print s.countPrimeSetBits(967080, 972754)
