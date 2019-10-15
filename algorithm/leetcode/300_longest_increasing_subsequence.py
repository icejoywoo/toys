#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/longest-increasing-subsequence/
    @author: icejoywoo
    @date: 2019-09-24
"""

# 暴力递归法，遍历所有的组合情况，然后算最大的，时间复杂度为2^n
class SolutionBF(object):

    result = set()

    def f(self, nums, a):
        if not nums:
            return self.result

        if len(a) == 0 or nums[0] > a[-1]:
            self.result.add(tuple(a+nums[:1]))
            self.f(nums[1:], a+nums[:1])

        self.result.add(tuple(a))
        self.f(nums[1:], a)

    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        self.result = set()
        self.f(nums, [])
        l = 0
        a = None
        for t in self.result:
            if len(t) > l:
                a = t
                l = len(t)
        return l


class Solution(object):
    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        l = len(nums)
        dp = [1 for _ in range(l)]

        for i in range(l):
            pre_dp = [dp[j] for j in range(i) if nums[i] > nums[j]]
            max_pre_dp = max(pre_dp) if pre_dp else 0
            dp[i] = max_pre_dp + 1

        return max(dp)


if __name__ == '__main__':
    s = Solution()
    assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert s.lengthOfLIS([]) == 0
    assert s.lengthOfLIS([0]) == 1
