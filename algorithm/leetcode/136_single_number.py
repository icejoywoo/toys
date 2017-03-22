#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/single-number/
    @author: wujiabin@baidu.com
    @date: 07/03/2017
"""


class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = nums[0]
        for i in nums[1:]:
            n ^= i
        return n


if __name__ == '__main__':
    s = Solution()
    assert s.singleNumber([1]) == 1
    assert s.singleNumber([1, 1, 2, 3, 4, 2, 3]) == 4
