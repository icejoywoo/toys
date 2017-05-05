#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 24/03/2017
"""


class Solution(object):

    mapping = {
        '1': '',
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz',
        '*': '+',
        '0': ' ',
        '#': '',
    }

    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """


        if digits:
            d = digits[0]
            chars = self.mapping[d]
            if len(digits) == 1:
                return list(self.mapping[d])
            else:
                result = []
                for c in chars:
                    for d in self.letterCombinations(digits[1:]):
                        result.append(c+d)
                return result
        else:
            return []


if __name__ == '__main__':
    s = Solution()
    print s.letterCombinations('23')
    print s.letterCombinations('234567')
