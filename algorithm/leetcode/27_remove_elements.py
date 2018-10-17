#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2018/10/17
"""


class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        i = 0
        l = len(nums)
        while i < l:
            if nums[i] == val:
                del nums[i]
                l -= 1
            else:
                i += 1
        return len(nums)


if __name__ == '__main__':
    s = Solution()
    assert s.removeElement([1], 1) == 0
    assert s.removeElement([1, 2, 3], 2) == 2
    assert s.removeElement([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 1) == 7
