#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: requests scrape proxy list and test proxy
    @author: icejoywoo
    @date: 04/05/2017
"""
import random

import requests
from pyquery import PyQuery as pq


def load_proxies():
    r = requests.get('http://www.kuaidaili.com/free/inha/')
    result = []
    if r.status_code == 200:
        d = pq(r.content)
        for item in d('table tr:gt(0)').items():
            ip = item('td:eq(0)').html().strip()
            port = item('td:eq(1)').html().strip()
            proxy = '%s:%s' % (ip, port)
            proxies = {
                'http': 'http://%s' % proxy,
                'https': 'https://%s' % proxy,
            }
            try:
                print('test proxy: %s' % proxy)
                r = requests.get('http://www.baidu.com/', proxies=proxies)
                if r.status_code == 200:
                    print('add proxy %s' % proxy)
                    result.append(proxy)
                else:
                    print('proxy: %s, status: %d' % (proxy, r.status_code))
            except requests.exceptions.ProxyError:
                print('proxy %s cannot work' % proxy)

    return result


proxies = load_proxies()


def get_proxies():
    if proxies:
        proxy = random.choice(proxies)
        return {
            'http': 'http://%s' % proxy,
            'https': 'https://%s' % proxy,
        }
    else:
        return None


for proxy in proxies:
    proxies = {
        'http': 'http://%s' % proxy,
        'https': 'https://%s' % proxy,
    }
    r = requests.get('http://www.baidu.com/', proxies=proxies)
    print r.status_code
