#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/9/2

__author__ = 'wujiabin'


class Solution(object):

    def isNumber(self, s):
        """
        :type s: str
        :rtype: bool
        """
        # remove heading and tailing
        s = s.strip()

        i = 0
        length = len(s)
        is_number = False
        # 0. 正负号 sign
        if i < length and s[i] in '+-':
            i += 1

        # 1. 小数点或exponent前面的部分
        while i < length and s[i] in '0123456789':
            i += 1
            is_number = True

        # 2. 处理小数点部分, 小数点只可以在exponent前面, 后面是非法的
        # 合法: 1.5e2, 非法: 1.5e1.2
        if i < length and s[i] == '.':
            i += 1
            # 2a. 小数点后面的部分, 可以有, 也可以没有, 比如 1.表示1.0, .1表示0.1, 单独的小数点是非法的
            while i < length and s[i] in '0123456789':
                i += 1
                is_number = True

        # 3. 处理exponent部分, 必须保证exponent之前是一个数
        if is_number and i < length and s[i] == 'e':
            i += 1
            # 例如: 1e是非法的, e的前后必须有数字
            is_number = False
            # 3a. 处理正负号
            if i < length and s[i] in '+-':
                i += 1
            # 3b. 处理exponent后面的部分, 必须是个正整数
            while i < length and s[i] in '0123456789':
                i += 1
                is_number = True

        # 必须保证整个字符串都匹配这个形式, i < length表示结尾有字符串不是数字
        return is_number and i == length

if __name__ == '__main__':
    s = Solution()
    assert not s.isNumber("")
    assert s.isNumber("0")
    assert s.isNumber(" 0.1 ")
    assert s.isNumber("3.")
    assert s.isNumber(".1")
    assert not s.isNumber(".")
    assert not s.isNumber("abc")
    assert not s.isNumber("1 a")
    assert s.isNumber("+1e4")
    assert s.isNumber("+1e-4")
    assert not s.isNumber("1e4.4")
    assert not s.isNumber("1e")
    assert not s.isNumber(".e1")
