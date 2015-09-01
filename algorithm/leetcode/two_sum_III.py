#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

"""
Design and implement a TwoSum class. It should support the following operations: add
and find.
add(input) – Add the number input to an internal data structure.
find(value) – Find if there exists any pair of numbers which sum is equal to the value.
For example,
add(1); add(3); add(5); find(4)  true; find(7)  false
"""


class TwoSum:

    def __init__(self):
        # v来计数
        self._map = {}

    def add(self, n):
        self._map.setdefault(n, 0)
        self._map[n] += 1
        return self

    def find(self, sum):
        for i, n in enumerate(self._map):
            gap = sum - n
            # 有可能gap和n相等， 需要有两个以上的相同数才可以
            if gap == n and self._map[gap] >= 2:
                return True
            elif gap != n and gap in self._map:
                return True
        return False


if __name__ == '__main__':
    print TwoSum().add(1).add(3).add(5).find(4)
    print TwoSum().add(1).add(3).add(5).find(7)