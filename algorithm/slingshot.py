#!/usr/bin/env python
# encoding: utf-8

# 问题：http://www.usaco.org/index.php?page=viewproblem2&cpid=816&lang=zh
# 官网解释：http://usaco.org/current/data/sol_slingshot_platinum_feb18.html
# 参考解法：https://blog.csdn.net/xujingyifuyunxiang/article/details/79997526


class SlingShot(object):

    def __init__(self, input):
        self._slingshot = []
        self._cow_dung = []

        slingshot_count, cow_dung_count = input.readline().split()
        for _ in range(int(slingshot_count)):
            self._slingshot.append([int(i) for i in input.readline().split()])

        for _ in range(int(cow_dung_count)):
            self._cow_dung.append([int(i) for i in input.readline().split()])

    def calc(self):
        result = []
        for cow_dung in self._cow_dung:
            base = abs(cow_dung[0] - cow_dung[1])

            for slingshot in self._slingshot:
                a = abs(cow_dung[0] - slingshot[0])
                b = abs(cow_dung[1] - slingshot[1])
                first = a + slingshot[2] + b

                c = abs(cow_dung[1] - slingshot[0])
                d = abs(cow_dung[0] - slingshot[1])
                second = c + slingshot[2] + d

                base = min(base, first, second)
            result.append(base)
        return result


if __name__ == '__main__':
    import StringIO

    test_input = StringIO.StringIO("""2 3
0 10 1
13 8 2
1 12
5 2
20 7""")
    s = SlingShot(test_input)
    print s.calc()
