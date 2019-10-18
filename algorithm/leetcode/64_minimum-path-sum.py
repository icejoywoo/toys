#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/minimum-path-sum/
    @author: icejoywoo
    @date: 2019-10-18
"""


class Solution(object):
    def minPathSum(self, grid):
        """
        DP
        :type grid: List[List[int]]
        :rtype: int
        """
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = grid[0][0]

        # first row
        for i in range(1, n):
            dp[0][i] = dp[0][i-1] + grid[0][i]

        # first column
        for i in range(1, m):
            dp[i][0] = dp[i-1][0] + grid[i][0]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]

        return dp[m-1][n-1]

    def minPathSumV1(self, grid):
        """
        DP
        :type grid: List[List[int]]
        :rtype: int
        """
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = grid[0][0]

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                a = float('inf') if i - 1 < 0 else dp[i - 1][j]
                b = float('inf') if j - 1 < 0 else dp[i][j - 1]
                dp[i][j] = min(a, b) + grid[i][j]

        return dp[m-1][n-1]

    def minPathSumRecursion(self, grid):
        """
        Timeout
        :type grid: List[List[int]]
        :rtype: int
        """
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        # down and right direction
        dxy = ((1, 0), (0, 1))

        def f(x, y, sum):
            if x == m-1 and y == n-1:
                return sum

            result = []
            for dx, dy in dxy:
                # valid path
                if 0 <= (x + dx) < m and 0 <= (y + dy) < n:
                    result.append(f(x + dx, y + dy, sum + grid[x + dx][y + dy]))
            return min(result)

        return f(0, 0, grid[0][0])

    def minPathSumRecursionWithPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        dxy = ((1, 0), (0, 1))

        def f(x, y, sum, path):
            if x == m-1 and y == n-1:
                print path
                return sum

            result = []
            for dx, dy in dxy:
                # valid path
                if 0 <= (x + dx) < m and 0 <= (y + dy) < n:
                    result.append(f(x + dx, y + dy, sum + grid[x + dx][y + dy], path + [(x + dx, y + dy)]))
            return min(result)

        return f(0, 0, grid[0][0], [(0, 0)])


if __name__ == '__main__':
    s = Solution()
    assert s.minPathSum([[1]]) == 1
    assert s.minPathSum([[0]]) == 0
    assert s.minPathSum([]) == 0
    assert s.minPathSum([[1, 2], [1, 1]]) == 3
    assert s.minPathSum([
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]) == 7

    assert s.minPathSum(
        [[7, 1, 3, 5, 8, 9, 9, 2, 1, 9, 0, 8, 3, 1, 6, 6, 9, 5],
         [9, 5, 9, 4, 0, 4, 8, 8, 9, 5, 7, 3, 6, 6, 6, 9, 1, 6],
         [8, 2, 9, 1, 3, 1, 9, 7, 2, 5, 3, 1, 2, 4, 8, 2, 8, 8],
         [6, 7, 9, 8, 4, 8, 3, 0, 4, 0, 9, 6, 6, 0, 0, 5, 1, 4],
         [7, 1, 3, 1, 8, 8, 3, 1, 2, 1, 5, 0, 2, 1, 9, 1, 1, 4],
         [9, 5, 4, 3, 5, 6, 1, 3, 6, 4, 9, 7, 0, 8, 0, 3, 9, 9],
         [1, 4, 2, 5, 8, 7, 7, 0, 0, 7, 1, 2, 1, 2, 7, 7, 7, 4],
         [3, 9, 7, 9, 5, 8, 9, 5, 6, 9, 8, 8, 0, 1, 4, 2, 8, 2],
         [1, 5, 2, 2, 2, 5, 6, 3, 9, 3, 1, 7, 9, 6, 8, 6, 8, 3],
         [5, 7, 8, 3, 8, 8, 3, 9, 9, 8, 1, 9, 2, 5, 4, 7, 7, 7],
         [2, 3, 2, 4, 8, 5, 1, 7, 2, 9, 5, 2, 4, 2, 9, 2, 8, 7],
         [0, 1, 6, 1, 1, 0, 0, 6, 5, 4, 3, 4, 3, 7, 9, 6, 1, 9]]) == 85
