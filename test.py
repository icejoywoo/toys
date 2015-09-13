#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

# 可以利用默认参数的特性，为函数提供一个缓存功能
def d(k, v=None, cache={}):
    if v:
        cache[k] = v
        return cache
    else:
        return cache.get(k, None), cache

print d("key")  # (None, {})
print d("key", "value")  # {'key': 'value'}
print d("key")  # ('value', {'key': 'value'})

# 利用闭包来实现类似功能

def _d():
    cache = {}
    def wrapper(k, v=None):
        if v:
            cache[k] = v
            return cache
        else:
            return cache.get(k, None), cache
    return wrapper

d = _d()

print d("key")  # (None, {})
print d("key", "value")  # {'key': 'value'}
print d("key")  # ('value', {'key': 'value'})

# 利用函数的magic method来实现
class D(object):

    def __init__(self):
        self.cache = {}

    def __call__(self, k, v=None):
        if v:
            self.cache[k] = v
            return self.cache
        else:
            return self.cache.get(k, None), self.cache

d = D()

print d("key")  # (None, {})
print d("key", "value")  # {'key': 'value'}
print d("key")  # ('value', {'key': 'value'})
