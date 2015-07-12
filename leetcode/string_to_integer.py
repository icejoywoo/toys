#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

class Solution:
    # @param {string} str
    # @return {integer}
    def myAtoi(self, str):
        str = str.strip()
        ret = 0
        sign_flag = False
        sign = 1
        for i, c in enumerate(str):
            if c in '0123456789':
                ret = (ord(c) - ord('0')) + ret * 10
            elif not sign_flag and c in '-+':
                sign_flag = True
                if c == '-':
                    sign = -1
            else:
                break
        result = ret * sign
        # integer overflow
        if result > 2147483647:  # 2*31 - 1
            return 2147483647
        elif result < -2147483648:  # -2*31
            return -2147483648
        else:
            return ret * sign


if __name__ == '__main__':
    assert Solution().myAtoi('+-2') == 0
    assert Solution().myAtoi('-12a34') == -12
    assert Solution().myAtoi("2147483648") == 2**31 - 1
    assert Solution().myAtoi("-2147483648") == -2**31
    assert Solution().myAtoi("-2147483649") == -2**31