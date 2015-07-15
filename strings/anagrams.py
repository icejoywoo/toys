#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

import string


def anagrams(a, b):
    """ 判断是否为重组词
    http://javarevisited.blogspot.sg/2013/03/Anagram-how-to-check-if-two-string-are-anagrams-example-tutorial.html
    :param a:
    :param b:
    :return:
    """

    if len(a) != len(b):
        return False

    pool = string.ascii_letters
    filtered_a = ''.join(sorted([i.lower() for i in a if i in pool]))
    filtered_b = ''.join(sorted([i.lower() for i in b if i in pool]))
    return filtered_a == filtered_b


if __name__ == '__main__':
    assert anagrams('Army', 'Mary')
    assert anagrams('stop', 'pots')
    assert not anagrams('stop', 'potsb')
    assert not anagrams('aa', 'aaaaaa')
