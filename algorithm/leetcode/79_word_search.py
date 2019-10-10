#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode-cn.com/problems/word-search/
    @author: icejoywoo
    @date: 2019-10-10
"""


class Solution(object):
    dx = (-1, 0, 1, 0)
    dy = (0, -1, 0, 1)

    def search(self, board, height, width, word, i, j, path=None):
        # word is empty
        if not word:
            return True

        if i < 0 or i >= height or j < 0 or j >= width:
            return False

        if path is None:
            path = set()

        if path and (i, j) in path:
            # print i, j, board[i][j], path
            return False

        # print i, j, board[i][j], word
        if board[i][j] == word[0]:
            for x in range(4):
                path.add((i, j))
                if self.search(board, height, width, word[1:], i + self.dx[x], j + self.dy[x], path):
                    return True
                path.remove((i, j))

        return False

    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        # board is empty
        if not board:
            return False

        # word is None or empty
        if not word:
            return True

        height = len(board)
        width = len(board[0])

        for i in range(height):
            for j in range(width):
                if self.search(board, height, width, word, i, j):
                    return True

        return False


if __name__ == '__main__':
    s = Solution()
    assert s.exist([
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]], "ABCCED")
    assert s.exist([
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]], "SEE")
    assert not s.exist([
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]], "ABCB")
    assert s.exist([
        ["A", "B", "C", "E"],
        ["S", "F", "E", "S"],
        ["A", "D", "E", "E"]], "ABCESEEEFS")