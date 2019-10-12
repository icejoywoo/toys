#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/maximum-product-subarray/
    @author: icejoywoo
    @date: 2019-10-12
"""
import sys


class Solution(object):
    def maxProductBF(self, nums):
        """
        暴力法，递归暴力法貌似无法实现？
        :type nums: List[int]
        :rtype: int
        """
        l = len(nums)

        m = -sys.maxint - 1

        for start in range(l):
            for length in range(1, l - start + 1):
                m = max(m, reduce(lambda a, b: a * b, nums[start:start+length]))

        return m

    def maxProductDP(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        l = len(nums)
        # negative abs max, positive max
        dp = [(0, 0)] * l
        dp[0], res = (nums[0], nums[0]), nums[0]

        for i in range(1, l):
            e = nums[i]
            if e >= 0:
                dp[i] = (min(dp[i-1][0] * e, e), max(dp[i-1][1] * e, e))
            else:
                dp[i] = (min(dp[i-1][1] * e, e), max(dp[i-1][0] * e, e))

        return max([i[1] for i in dp])

    def maxProductDP2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        l = len(nums)
        # negative abs max, positive max
        # 只需要两个状态即可，可以压缩状态
        dp = [(0, 0)] * 2
        dp[0], res = (nums[0], nums[0]), nums[0]

        for i in range(1, l):
            e = nums[i]
            x, y = i % 2, (i-1) % 2
            dp[x] = (
                min(dp[y][0] * e, dp[y][1] * e, e),
                max(dp[y][1] * e, dp[y][0] * e, e)
            )
            if dp[x][1] > res:
                res = dp[x][1]

        return res

    maxProduct = maxProductDP2


if __name__ == '__main__':
    s = Solution()
    assert s.maxProduct([2, 3, -2, 4]) == 6
    assert s.maxProduct([-2, 2, 3, 4]) == 24
    assert s.maxProduct([-2, 0, -1]) == 0
    assert s.maxProduct([-2]) == -2
    assert s.maxProduct([-2, 3, -4]) == 24
    assert s.maxProduct([0, 2]) == 2
    assert s.maxProduct([1,-5,6,-5,2,-4,-5,0,3,2,-4,0,-5,-3,-1,-4,-1,4,1,-1,-3,-1,1,3,-4,-6,-2,5,1,-5,0,-1,-5,0,1,2,6,1,2,-6,5,5,0,1,0,1,1,-1,-1,3,1,0,4,-3,0,4,-4,-1,6,5,5,6,-6,1,1,3,4,3,-1,-3,0,-5,-4,1,5,-2,3,-1,2,1,1,6,0,5,-5,6,-6,3,0,4,-1,3,6,0,-2,0,-1,6,4,1,-5,1,0,1,-1,-1,3,5,5,4,2,5,0,-1,5,2,2,-3,-1,-1,0,-6,-2,-5,1,-2,2,0,0,2,-3,-2,-4,1,1,-4,-3,-1,0,0,1,-3,-2,3,-4,5,2,-1,4,1,5,6,0,1,1,-2,-1,0,-1,-5,5,6,6,-1,-1,0,-4,2,1,3,-5,6,-5,-1,-1,-3,-1,-4,-2,-1,-1,1,-3,-4,0,1,-3,4,3,2,-2,6,-3,-6,-6,-2,-5,1,2,0,-1,0,0,-2,3,-4,2,4,3,-1,3,1,0,2,1,-1,0,5,-1,-3,-6,-5,0,6,6,-6,-5,4,-2,-1,0,4,6,-3,1,-1,0,1,-5,5,-3,-3,-3,-1,-1,4,0,-2,-4,3,5,5,-1,-1,-5,-2,-4,-4,6,0,-3,-1,-5,-3,-1,6,1,-5,-1,0,1,-4,-5,0,0,0,-3,-5,-1,-4,-1,5,5,-4,4,-1,6,-1,1,-1,2,-2,-3,0,1,0,0,-3,0,2,5,-6,-3,-3,3,-4,-2,-6,-1,1,4,4,0,-6,-5,-6,-3,5,-3,1,-4,6,-2,0,-4,-1,0,-1,0,6,-6,0,5,0,1,-3,6,1,-1,1,0,-1,1,-1,-6,-3,4,-1,-4,6,4,-1,-3,2,-6,5,0,4,-2,1,0,4,-2,2,0,0,5,5,-3,4,3,-5,2,2,6,-1,-2,1,-3,1,-1,6,-4,0,0,0,2,-5,-4,2,6,-3,-6,-1,-6,0,0,2,-1,6,-4,-5,-1,0,-3,-3,-1,0,-4,3,1,5,0,2,5,0,4,-5,-1,3,1,-1,-1,1,1,-2,3,5,4,6,2,6,-6,5,2,-3,0,-1,-1,3,1,1,1,-2,-5,3,-1,3,0,-1,3,1,1,-2,6,3,-6,5,-5,-5,0,-2,-3,-3,-4,6,-1,-6,6,-3,-5,1,-1,0,0,1,4,-5,0,1,-2,6,1,-3,-5,0,4,-2,1,-5,-4,0,0,-1,-2,0,2,-2,5,6]) == 31104000
