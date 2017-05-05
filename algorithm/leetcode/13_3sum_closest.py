#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/3sum-closest/?tab=Description
    @author: icejoywoo
    @date: 07/03/2017
"""


class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        result = None
        for i in xrange(len(nums) - 2):
            # 退化为求解 2sum 的问题
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[l] + nums[r] + nums[i]
                if result is None or abs(s - target) < abs(result - target):
                    result = s
                if s <= target:
                    l += 1
                else:
                    r -= 1
        return result


if __name__ == '__main__':
    s = Solution()
    assert s.threeSumClosest([-1, 2, 1, -4], 1) == 2
    assert s.threeSumClosest(
        [47, -48, -72, 97, -78, 50, -22, 18, 9, 24, 28, -53, 44, -96, 50, 45, 86, 11, 21, -44, 67, 83, 55, -86, -33, 0,
         -53, -94, -60, 57, -72, -73, -27, 13, 91, 80, 18, -80, -29, -69, -74, -90, 54, 22, 3, 91, -47, -32, 80, -55,
         69, -95, 62, -92, 4, -86, 62, 3, 23, -30, -4, 0, 49, 24, 10, -32, 79, -99, -66, -30, -83, -13, 90, -27, 9, -4,
         9, 98, -70, -19, 32, 24, -77, 83, 11, -78, -94, 4, 41, 61, 20, 96, -36, 54, -46, -51, 91, 54, 30, -42, 82, 0,
         9, 24, -2, 32, -16, -18, 87, 23, 78, -10, -82, -67, 68, -18, -61, 91, -90, -53, 67, -48, 12, 1, -71, -99, 31,
         82, 39, -56, 23, -89, -58, 19, -60, 39, -23, -76, -85, 67, -33, 69, -74, -8, -99, 52, -70, -71, 85, -8, 28, -3,
         -100, 18, 88, 5, -16, 17, 91, -35, 22, -76], 298) == 291
    assert s.threeSumClosest([1, 1, -1], 0) == 1
    assert s.threeSumClosest([0,2,1,-3], 1) == 0
