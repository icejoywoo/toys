#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 16/4/19
"""

import fcntl
import multiprocessing
import socket


def close_on_exec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    flags |= fcntl.FD_CLOEXEC
    fcntl.fcntl(fd, fcntl.F_SETFD, flags)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 1880))
s.listen(1)

close_on_exec(s)


def foo():
    # socket 并没有关闭
    import time
    time.sleep(600)


p = multiprocessing.Process(target=foo)
p.daemon = True
p.start()
p.join()
