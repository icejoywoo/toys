#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: a simple rpc client implementation
    http://python3-cookbook.readthedocs.io/zh_CN/latest/c11/p08_implementing_remote_procedure_calls.html
    @author: icejoywoo@gmail.com
    @date: 11/01/2017
"""

import pickle


class RPCProxy(object):

    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc


from multiprocessing.connection import Client

c = Client(('localhost', 17000), authkey=b'peekaboo')
proxy = RPCProxy(c)
print proxy.add(2, 3)
print proxy.sub(2, 3)
print proxy.sub([1, 2], 4)