#!/bin/env python
# encoding: utf-8
"""
https://leetcode.com/problems/integer-to-roman/description/
"""

roman_numbers = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

class Solution(object):

    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """