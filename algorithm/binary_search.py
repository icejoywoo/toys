#!/usr/bin/env python
# encoding: utf-8


def binary_search_v1(sorted_list, element, _cmp=None):
    """ 二分查找
    :param sorted_list: 有序列表
    :param element: 查找元素
    :param _cmp: 比较函数，默认使用 builtin cmp
    :return: 如果存在，返回索引值，否则返回 None
    """
    p, q = 0, len(sorted_list) - 1
    i = (p + q) / 2

    _cmp = _cmp if _cmp else cmp

    while p <= i <= q:
        cmp_ret = _cmp(sorted_list[i], element)
        if cmp_ret == 0:
            return i
        elif cmp_ret > 0:
            q = i - 1
            i = (p + q) / 2
        else:  # cmp_ret < 0
            p = i + 1
            i = (p + q) / 2

    # not found
    return None


def binary_search_v2(sorted_list, element, _cmp=None):
    """ 二分查找
    :param sorted_list: 有序列表
    :param element: 查找元素
    :param _cmp: 比较函数，默认使用 builtin cmp
    :return: 如果存在，返回索引值，否则返回 None
    """
    import bisect
    i = bisect.bisect_left(sorted_list, element, lo=0, hi=len(sorted_list) - 1)
    if sorted_list[i] == element:
        return i
    else:
        return None


if __name__ == '__main__':
    def simple_test(binary_search):
        l = [1, 4, 5, 6, 8, 10, 34]
        assert binary_search(l, 1) == 0
        assert binary_search(l, 34) == 6
        assert binary_search(l, 5) == 2
        assert binary_search(l, 2) is None
    simple_test(binary_search_v1)
    simple_test(binary_search_v2)
