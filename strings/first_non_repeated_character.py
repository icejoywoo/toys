#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


def first_non_repeated_character(s):
    """
    http://javarevisited.blogspot.sg/2014/03/3-ways-to-find-first-non-repeated-character-String-programming-problem.html
    :param s:
    :return:
    """
    repeating = []
    non_repeated = []
    for i in s:
        if i in repeating:
            continue

        if i in non_repeated:
            non_repeated.remove(i)
            repeating.append(i)
        else:
            non_repeated.append(i)
    return non_repeated[0] if non_repeated else None


if __name__ == '__main__':
    assert first_non_repeated_character('Morning') == 'm'
