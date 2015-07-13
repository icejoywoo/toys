#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

# Similar to Question [1. Two Sum], except that the input array is already sorted in
# ascending order.

class Solution:
    # @param {integer[]} nums
    # @param {integer} target
    # @return {integer[]}
    def twoSum(self, nums, target):

        def bisearch(n, array, start, end):
            l = start
            r = end
            while l < r:
                mid = (l + r) / 2
                if array[mid] > n:
                    r = mid
                elif array[mid] < n:
                    l = mid + 1
                elif array[mid] == n:
                    return mid
            return -1

        for i, n in enumerate(nums):
            gap = target - n
            print gap, nums, i+1, len(nums)-1
            index = bisearch(gap, nums, i+1, len(nums)-1)
            if index != -1:
                return i, index


if __name__ == '__main__':
    print Solution().twoSum([1, 2, 3, 4, 5, 6], 5)
