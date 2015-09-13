#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

class Solution:

    def missing_ranges(self, array, start=0, end=99):

        def _array_wrapper():
            yield start-1
            for i in array:
                yield i
            yield end+1

        ranges = []
        first_iter = _array_wrapper()
        second_iter = _array_wrapper()
        second_iter.next()
        for start, end in zip(first_iter, second_iter):
            if end - start == 2:
                ranges.append('%d' % (start+1))
            elif end - start > 2:
                ranges.append('%d->%d' % (start+1, end-1))

        return ranges


if __name__ == '__main__':
    s = Solution()
    assert s.missing_ranges(range(100)) == []
    assert s.missing_ranges([0]) == ['1->99']
    assert s.missing_ranges([99]) == ['0->98']
    assert s.missing_ranges([56]) == ['0->55', '57->99']
    assert s.missing_ranges([]) == ['0->99']
    assert s.missing_ranges([0, 1, 3, 50, 75]) == ['2', '4->49', '51->74', '76->99']

    assert s.missing_ranges(range(1000), 0, 999) == []
    assert s.missing_ranges([555], 0, 999) == ['0->554', '556->999']
