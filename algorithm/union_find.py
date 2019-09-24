#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2019-09-24
"""

# 并查集
class UnionFind(object):

    def __init__(self, size):
        self.roots = [i for i in xrange(size)]

    def find(self, x):
        r = x
        while r != self.roots[r]:
            r = self.roots[r]

        # path compression
        # 遍历一次，将路径上的节点父节点都指向同一个root，减少路径长度
        i = x
        while i != self.roots[i]:
            i, self.roots[i] = self.roots[i], r

        return r

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def union(self, x, y):
        a, b = self.find(x), self.find(y)
        self.roots[a] = b


if __name__ == '__main__':
    u = UnionFind(20)
    assert u.connected(0, 1) is False
    assert u.connected(0, 10) is False
    u.union(0, 1)
    u.union(0, 10)
    assert u.connected(0, 1)
    assert u.connected(1, 10)

    u.union(2, 5)
    u.union(5, 4)
    assert u.connected(2, 4)

    assert u.connected(2, 10) is False
