#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 9/20/16
"""

import threading


class Counter(object):

    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


class LockCounter(object):

    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self, offset):
        with self._lock:
            self.count += offset


def worker(i, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = threading.Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    how_many = 10**5
    counter = Counter()
    run_threads(worker, how_many, counter)
    print('Counter without lock should be %d, found %d.' % (5 * how_many, counter.count))

    counter = LockCounter()
    run_threads(worker, how_many, counter)
    print('Counter with lock should be %d, found %d.' % (5 * how_many, counter.count))
