#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {integer[]} nums
    # @param {integer} target
    # @return {integer[]}
    def twoSum(self, nums, target):
        nums_dict = {n:i for i, n in enumerate(nums)}
        for i, n in enumerate(nums):
            gap = target - n
            if gap in nums_dict and nums_dict[gap] != i:
                return i + 1, nums_dict[gap] + 1
        return None


if __name__ == '__main__':
    s = Solution()
    print s.twoSum([4, 4], 8)
    print s.twoSum([4, 4, 4], 8)
