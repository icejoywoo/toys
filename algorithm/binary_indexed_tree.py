#!/usr/bin/env python
# encoding: utf-8

# https://blog.csdn.net/Yaokai_AssultMaster/article/details/79492190
# https://www.youtube.com/watch?v=v_wj_mOAlig
# 树状数组


class BIT(object):

    def __init__(self, array):
        self._bit = [0]
        self._bit += array
        self.length = len(self._bit)

        for i, e in enumerate(self._bit):
            j = i + (i & -i)
            if j < self.length:
                self._bit[j] += e

    def update(self, i, delta):
        index = i + 1
        while i < self._bit:
            self._bit[index] += delta
            index = index + (index & -index)

    def prefix_sum(self, i):
        index = i + 1
        result = 0
        while index > 0:
            result += self._bit[index]
            index = index - (index & -index)
        return result

    def range(self, from_i, to_i):
        return self.prefix_sum(to_i) - self.prefix_sum(from_i - 1)


if __name__ == '__main__':
    a = [1, 7, 3, 0, 5, 8, 3, 2, 6, 2, 1, 1, 4, 5]
    b = BIT(a)
    print b.prefix_sum(0)
    print b.range(0, 7)

