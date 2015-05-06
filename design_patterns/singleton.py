#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/5/4

__author__ = 'wujiabin'


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return it


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


if __name__ == '__main__':
    class Test1(Singleton):
        a = 5

        def __init__(self, b=6):
            self.b = b

    @singleton
    class Test2(object):
        def __init__(self, a=1, b=2):
            self.a = a
            self.b = b

    a = Test1()
    print a.a, a.b
    b = Test1()
    b.a = 1
    b.b = 4
    print a.a, a.b, b.a, b.b

    c = Test2()
    print c.a, c.b
    d = Test2()
    d.a = 30
    d.b = 40
    print c.a, c.b, d.a, d.b
