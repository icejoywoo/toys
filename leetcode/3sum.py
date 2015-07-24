#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {integer[]} nums
    # @return {integer[][]}
    def threeSum(self, nums):

        result = []
        # 排序
        nums.sort()
        length = len(nums)

        i = 0
        while i < length - 2:
            while i < length - 2 and nums[i] == nums[i+1]:
                i += 1

            target = -nums[i]
            p = i + 1
            q = length - 1
            while p < q:
                if nums[p] + nums[q] > target:
                    q -= 1
                elif nums[p] + nums[q] < target:
                    p += 1
                else:
                    result.append([nums[i], nums[p], nums[q]])
                    # remove duplicate
                    while p < q and nums[p] == nums[p+1]:
                        p += 1
                    while p < q and nums[q] == nums[q-1]:
                        q -= 1
                    p += 1
                    q -= 1
            i += 1

        return result


if __name__ == '__main__':
    s = Solution()
    print s.threeSum([0, 0, 0, 0, 0]) == []
    print s.threeSum([-5, -4, -4, 1, 2, 3, 4, 5])
    print s.threeSum([-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6]) #== [[-4,-2,6],[-4,0,4],[-4,1,3],[-4,2,2],[-2,-2,4],[-2,0,2]]