#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'


def dulipcate_chars(s):
    """
    http://java67.blogspot.sg/2014/03/how-to-find-duplicate-characters-in-String-Java-program.html
    :param s:
    :return:
    """
    if s:
        result = {}
        for i in s:
            result.setdefault(i, 0)
            result[i] += 1

        for k, v in result.items():
            if v > 1:
                print k, v
    else:
        # None
        return None


if __name__ == '__main__':
    dulipcate_chars('')
    dulipcate_chars(None)
    dulipcate_chars('aa')
    dulipcate_chars('aaa')
