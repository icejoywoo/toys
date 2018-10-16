#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2018/10/16
"""


class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        last = None
        i = 0
        while i < len(nums):
            if nums[i] == last:
                del nums[i]
            else:
                last = nums[i]
                i += 1
        return len(nums)


if __name__ == '__main__':
    s = Solution()
    assert s.removeDuplicates([1]) == 1
    assert s.removeDuplicates([1, 2, 3]) == 3
    assert s.removeDuplicates([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]) == 5
