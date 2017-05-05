#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/5/4

__author__ = 'icejoywoo'

import random
import string

from hash_ring import HashRing


memcache_servers = ['192.168.0.246:11212',
                    '192.168.0.247:11212',
                    '192.168.0.249:11212']

weights = {
    '192.168.0.246:11212': 1,
    '192.168.0.247:11212': 2,
    '192.168.0.249:11212': 1
}

# simple
# ring = HashRing(memcache_servers)
# with weights
ring = HashRing(memcache_servers, weights)
iterations = 100000


def gen_code(length=10):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])


def random_distribution():
    counts = {}
    for s in memcache_servers:
        counts[s] = 0

    for _ in range(iterations):
        word = gen_code(10)
        counts[ring.get_node(word)] += 1

    for k in counts:
        print '%s: %s' % (k, counts[k])

random_distribution()
