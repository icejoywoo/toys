#!/usr/bin/env python
# encoding: utf-8
""" 斐波那契数列的各种实现

https://www.geeksforgeeks.org/program-for-nth-fibonacci-number/
"""


def fib_recursive(n):
    """ 递归实现的fib数列
    """
    # recursive terminator
    if n in (0, 1):
        return 1
    else:
        # process
        return fib_recursive(n-1) + fib_recursive(n-2)


def fib_recursive_with_cache(n, cache={}):
    """ 带有缓存的递归实现的fib数列
    """
    # recursive terminator
    if n in (0, 1):
        return 1

    # process
    if n - 1 not in cache:
        cache[n - 1] = fib_recursive_with_cache(n - 1)

    a = cache[n - 1]

    if n - 2 not in cache:
        cache[n - 2] = fib_recursive_with_cache(n - 2)

    b = cache[n - 2]
    return a + b


def fib_tail_recursive(n):
    """ 尾递归实现的fib数列
    """
    def _f(n, a, b):
        # recursive terminator
        if n in (0, 1):
            return b

        # process
        return _f(n-1, b, a+b)

    return _f(n, 1, 1)


def fib_iterate(n):
    """ 迭代实现的fib
    """
    if n <= 1:
        return 1

    f = [1, 1] + [0] * (n-1)

    for i in xrange(2, n+1):
        f[i] = f[i-1] + f[i-2]

    return f[n]


def fib_iterate2(n):
    """ 迭代实现的fib
    """
    if n <= 1:
        return 1

    a, b = 1, 1

    for i in xrange(2, n+1):
        a, b = b, a+b

    return b


def power_bruce_force(a, n):
    """ 暴力法实现的a的n次方
    """
    r = 1
    for _ in xrange(n):
        r *= a
    return r


def power_recursive(a, n):
    """ 二分递归实现的a的n次方，时间复杂度 log(n)
    """
    if n < 0:
        if a == 0:
            raise ArithmeticError("a cannot be zero when n is negative")
        else:
            return 1 / power_recursive(a, -n)

    if n == 0:
        return 1

    r = power_recursive(a, n / 2)
    # n % 2 == 0
    if n & 1 == 0:
        return r*r
    else:
        return r*r*a


def power_iterate(a, n):
    """ 二进制位操作迭代实现的a的n次方，时间复杂度 log(n)
    """
    if n < 0:
        if a == 0:
            raise ArithmeticError("a cannot be zero when n is negative")
        else:
            return 1 / power_iterate(a, -n)

    if n == 0:
        return 1

    i = n
    tmp = a
    result = 1
    while i != 0:
        # 判断最后一位为1
        if i & 1 == 1:
            result *= tmp

        i >>= 1
        # 二进制位迭代之后，每个1代表的数量不同，最开始的四维为：8 4 2 1
        tmp *= tmp
    return result


if __name__ == '__main__':
    for f in (fib_recursive, fib_recursive_with_cache, fib_tail_recursive, fib_iterate, fib_iterate2):
        assert f(0) == 1
        assert f(1) == 1
        assert f(10) == 89

    for p in (power_bruce_force, power_recursive, power_iterate):
        assert p(2, 3) == 8
        assert p(2, 0) == 1
        assert p(2, 10) == 1024
