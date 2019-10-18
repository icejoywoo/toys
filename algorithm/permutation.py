#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 全排列
    @author: icejoywoo
    @date: 2019-10-18
"""

import itertools


def permutation(l, size=None):
    l = list(l)
    size = len(l) if size is None else size

    def f(a, options):
        if len(a) == size:
            return [tuple(a)]
        else:
            result = []
            for i, e in enumerate(options):
                result += f(a + [e], options[:i] + options[i+1:])
            return result

    return f([], l)


def permutation2(l, size=None):
    l = list(l)
    size = len(l) if size is None else size

    def f(a, options, result):
        if len(a) == size or len(options) == 0:
            result.append(tuple(a))
        else:
            [f(a + [e], options[:i] + options[i+1:], result) for i, e in enumerate(options)]

    result = []
    f([], l, result)
    return result


# itertools.permutations 文档中标记的等价代码
def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    # 死循环
    while True:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


if __name__ == '__main__':
    print permutation('ABC')
    print permutation2('ABC')
    print permutation('ABC', 2)
    print list(permutations('ABC', 2))
    print list(itertools.permutations('ABC', 2))

    print permutation('ABCD', 2)
    print list(itertools.permutations('ABCD', 2))
