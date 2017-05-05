#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 爬取二手房网签信息的数据
    @author: icejoywoo
    @date: 03/05/2017
"""

import scrapy


class DmozSpider(scrapy.Spider):
    name = 'gzfang'
    allowed_domains = ['laho.gov.cn']
    start_urls = [
        'http://www.laho.gov.cn/g4cdata/search/laho/clfSearch.jsp',
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
