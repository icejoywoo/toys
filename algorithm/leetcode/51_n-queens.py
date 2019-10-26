#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/n-queens/
    @author: icejoywoo
    @date: 2019-10-19
"""


class Solution(object):
    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """

        results = []
        # 列
        col = set()
        # 斜线，撇
        pie = set()
        # 反斜线，捺
        na = set()

        def dfs(result, row):
            # terminator
            if row >= n:
                results.append(result)
                return

            for j in range(n):
                if j in col or row - j in pie or row + j in na:
                    continue

                col.add(j)
                pie.add(row - j)
                na.add(row + j)

                dfs(result + [j], row+1)

                col.remove(j)
                pie.remove(row - j)
                na.remove(row + j)

        dfs([], 0)

        return [['.' * i + 'Q' + (n-i-1) * '.' for i in r] for r in results]


if __name__ == '__main__':
    s = Solution()
    assert s.solveNQueens(4) == [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
