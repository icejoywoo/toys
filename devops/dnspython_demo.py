#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

import httplib
import os
import sys
import traceback

import dns.resolver


def get_iplist(domain):
    try:
        a = dns.resolver.query(domain, 'A')
    except:
        print >> sys.stderr, traceback.format_exc()
        raise

    ip_list = []
    # api的变化，与书中的示例不同
    for i in a:
        ip_list.append(i.address)
    return ip_list


def check_ip(ip, domain):
    check_url = '%s:80' % ip
    httplib.socket.setdefaulttimeout(5)
    conn = httplib.HTTPConnection(check_url)

    try:
        conn.request('GET', '/', headers={'Host': domain})
        r = conn.getresponse()
        content = r.read(15)
        if content == '<!doctype html>':
            print '%s [OK]' % ip
        else:
            print '%s [ERROR]' % ip
    finally:
        conn.close()


if __name__ == '__main__':
    domain = 'www.google.com'
    ip_list = get_iplist(domain)
    if ip_list and len(ip_list) > 0:
        for ip in ip_list:
            check_ip(ip, domain)
    else:
        print >> sys.stderr, "dns resolver error"
