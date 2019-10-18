#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/sqrtx/
    @author: icejoywoo
    @date: 2019-10-18
"""


class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        low = 0
        high = x
        ans = None
        while low <= high:
            mid = (low + high) / 2
            if mid ** 2 == x:
                ans = mid
                break
            elif mid * mid > x:
                high = mid - 1
            else:
                ans = mid
                low = mid + 1

        return ans


if __name__ == '__main__':
    s = Solution()
    assert s.mySqrt(1) == 1
    assert s.mySqrt(0) == 0
    assert s.mySqrt(4) == 2
    assert s.mySqrt(16) == 4
    assert s.mySqrt(8) == 2  # The square root of 8 is 2.82842..., and since the decimal part is truncated, 2 is returned.
