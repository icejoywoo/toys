#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: wujiabin@baidu.com
    @date: 22/03/2017
"""


class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)


class FilterMetaclass(UpperAttrMetaclass):
    def __new__(cls, name, bases, dct):
        attrs = {name: value for name, value in dct.items() if name not in ('reserved', 'sys')}
        return super(FilterMetaclass, cls).__new__(cls, name, bases, attrs)


class T(object):
    """ test

    """
    __metaclass__ = FilterMetaclass

    a = 1
    reserved = 2
    sys = 3

    def __init__(self):
        pass

print T.__dict__

