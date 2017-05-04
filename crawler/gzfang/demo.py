#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: crawl gz second-hand apartment info
    @author: icejoywoo
    @date: 03/05/2017
"""

import argparse
import datetime
import logging
import multiprocessing
from multiprocessing.dummy import Pool
import os
import random
import re
import sys
import urlparse

import pymongo
import requests
from retrying import retry
from pyquery import PyQuery as pq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FORMAT = '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(process)d %(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

START_URL = 'http://www.laho.gov.cn/g4cdata/search/laho/clfSearch.jsp'

RAND_URL = 'http://www.laho.gov.cn/g4cdata/search/generateRand.jsp'

OUTPUT = os.path.join(BASE_DIR, 'output.json')

mongo = pymongo.MongoClient('mongodb://localhost:27017/gzfang')

coll = mongo.gzfang.gzfang


class FailedToGetRandomException(Exception):
    pass

agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]


def get_headers():
    return {
        'User-Agent': random.choice(agents),
    }


@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000)
def get_random():
    """ read the f**king code """
    r = requests.get(RAND_URL, params={'randomId': random.uniform(0, 10000000)}, headers=get_headers())
    logger.debug('get random url: %s' % r.url)
    if r.status_code == 200:
        # 验证码, 随机输入
        imagevalue, clfrandinput = r.content.split('=')
        return imagevalue, clfrandinput
    else:
        logger.error('failed to get random. [status=%r]' % r.status_code)


def get_number(pattern, content):
    m = re.search(pattern, content)
    if m:
        return int(m.group(1))
    else:
        return None


@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000)
def load_page(page_number, start_date='', end_date=''):
    logger.debug('crawling page: %d' % page_number)
    imagevalue, clfrandinput = get_random()
    post_data = {
        'chnlname': '%B4%E6%C1%BF%B7%BF%B7%BF%D4%B4',  # GBK 编码
        'clfrandinput': clfrandinput,
        'currPage': page_number,
        'fbrqStart': start_date,  # 发布起始日期 eg. 2017-05-01
        'fbrqEnd': end_date,  # 发布结束日期 eg. 2017-05-02
        'fbzl': '',  # 发布坐落
        'fwyt': '-1',
        'hxcf': '-1',
        'hxs': '-1',
        'hxt': '-1',
        'hxw': '-1',
        'hxyt': '-1',
        'imgvalue': imagevalue,
        'jgfwStart': '-1',
        'judge': '1',
        'jyzt': '-1',  # 交易状态: -1 全部,0 放盘,1 已签约,2 已递件,3 已结案
        'jzmjStart': '-1',  # 建筑面积: -1 全部,1 30平方米以下,2 30～50平方米,3 50～70平方米,4 70～90平方米,5 90～120平方米,6 120～144平方米,7 144平方米以上
        'orderfield': '',
        'ordertype': '',
        'pybh': '',  # 盘源编号 text input
        'xqmc': '',  # 小区名称 text input
        'xzqh': '-1',  # 行政区域: -1 全部,03 荔湾区,04 越秀区,05 海珠区,06 天河区,11 白云区,12 黄埔区,13 番禺区,14 花都区,16 罗岗区,17 南沙区
        'zjfwjgmc': '',  # 中介机构, text input
    }

    r = requests.post(START_URL, data=post_data, headers=get_headers())
    logger.debug('url: %r, status: %r, charset: %r' % (r.url, r.status_code, r.encoding))
    d = pq(r.content)

    # 页面显示的页数，翻页可能预期页数与实际页数不一致
    current_page = get_number(ur'当前第(\d+)页'.encode(r.encoding), r.content)
    total_page = get_number(ur'总共(\d+)页'.encode(r.encoding), r.content)

    assert current_page == page_number + 1

    keys = ('fang_id', 'district', 'location', 'price', 'layout', 'square_meter', 'state', 'agency', 'publish_date')

    counter = 0
    for element in d('#tab tr').items():
        # skip first column 'index'
        values = [i.text() for i in element('td').items()][1:]
        if values:
            data = dict(zip(keys, values))
            data['_id'] = data['fang_id']
            data['details_url'] = urlparse.urljoin(START_URL, element('td:eq(1) a').attr('href'))
            ret = coll.save(data)
            logger.debug('ret: %r, insert data: %r, ' % (ret, data))
            counter += 1
        else:
            logger.debug('cannot parse line: %r' % element.html())
    logger.info('start date: %(start_date)r, end date: %(end_date)r, '
                'page: %(current_page)r, data count: %(counter)r' % locals())
    return current_page, total_page

if __name__ == '__main__':

    date_format = '%Y-%m-%d'

    def valid_date(s):
        try:
            return datetime.datetime.strptime(s, date_format)
        except ValueError:
            raise argparse.ArgumentTypeError('Not a valid date: {0}.'.format(s))


    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--start_date",
                        help="The Start Date - format YYYY-MM-DD ",
                        required=True,
                        type=valid_date)
    parser.add_argument('-e', "--end_date",
                        help="The End Date - format YYYY-MM-DD ",
                        required=False,
                        type=valid_date)
    args = parser.parse_args()
    logger.info('args: %r' % args)

    today = datetime.datetime.combine(datetime.datetime.today(), datetime.time())

    start_date = args.start_date if args.start_date else today
    end_date = args.end_date if args.end_date else args.start_date
    interval = (end_date - start_date).days

    def start_process():
        logger.debug('starting process: %s' % multiprocessing.current_process().name)

    pool = Pool(processes=multiprocessing.cpu_count(), initializer=start_process)

    try:
        for i in range(interval+1):
            page_start_date = (start_date + datetime.timedelta(days=i)).strftime(date_format)
            page_end_date = (start_date + datetime.timedelta(days=i+1)).strftime(date_format)
            current_page, total_page = load_page(0, page_start_date, page_end_date)
            logger.info('start date: %(page_start_date)r, end date: %(page_end_date)r, '
                        'page: %(current_page)r, total: %(total_page)r' % locals())
            for j in xrange(1, total_page):
                pool.apply_async(load_page, (j, page_start_date, page_end_date))

        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        logger.warn('Caught user cancel signal and exiting.')
        sys.exit(1)
