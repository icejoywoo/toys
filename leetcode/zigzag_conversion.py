#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


class Solution:
    # @param {string} s
    # @param {integer} numRows
    # @return {string}
    def convert(self, s, numRows):
        gap = numRows - 2
        result = [[] for _ in range(numRows)]
        i = iter(s)
        try:
            while True:
                for j in range(numRows):
                    result[j].append(i.next())
                for j in range(gap, 0, -1):
                    result[j].append(i.next())
        except StopIteration:
            pass
        return ''.join([''.join(i) for i in result])


if __name__ == '__main__':
    print Solution().convert("PAYPALISHIRING", 3) == 'PAHNAPLSIIGYIR'
