#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: crawl gz second-hand apartment info
    @author: icejoywoo
    @date: 03/05/2017
"""

import argparse
import collections
import datetime
import logging
import multiprocessing
from multiprocessing.dummy import Pool
import os
import random
import re
import sys
import traceback
import urlparse

import requests
import sqlalchemy.exc
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import attributes, sessionmaker
from retrying import retry
from pyquery import PyQuery as pq

import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('demo')
log.setup_logger(logger, workspace=BASE_DIR, level=logging.INFO)

START_URL = 'http://www.laho.gov.cn/g4cdata/search/laho/clfSearch.jsp'

RAND_URL = 'http://www.laho.gov.cn/g4cdata/search/generateRand.jsp'

OUTPUT = os.path.join(BASE_DIR, 'output.json')

engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'sqlite3.db'))
Base = declarative_base()


class Fang(Base):
    __tablename__ = 'gzfang'

    fang_id = Column('fang_id', String, primary_key=True)
    district = Column('district', String, nullable=True)
    location = Column('location', String, nullable=True)
    price = Column('price', Float, nullable=True)
    layout = Column('layout', String, nullable=True)
    square_meter = Column('square_meter', Float, nullable=True)
    state = Column('state', String)
    agency = Column('agency', String)
    publish_date = Column('publish_date', String)
    details_url = Column('details_url', String)  # 详情页 url

    def __init__(self, **kwargs):
        columns = {c.name: c for c in Fang.__table__.columns}
        unknown_columns = []
        for k, v in kwargs.items():
            if k in columns:
                setattr(self, k, v)
            else:
                unknown_columns.append((k, v))
        if unknown_columns:
            logger.debug('Unknown column: %s' % ','.join(['%r=%r' % (k, v) for k, v in unknown_columns]))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in Fang.__table__.columns}

    def diff(self):
        """ http://stackoverflow.com/questions/3645802/how-to-get-the-original-value-of-changed-fields """
        r = {}
        for c in Fang.__table__.columns:
            h = attributes.get_history(self, c.name)
            if h.has_changes():
                r[c.name] = (h.deleted, h.added)
        return r

    def diff_str(self):
        return ','.join(['%s("%s" to "%s")' % (k, '|'.join(v[0]), '|'.join(v[1])) for k, v in self.diff().items()])

    def __repr__(self):
        return '<Fang(id=%r)>' % self.fang_id

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


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
        return 1


def handle(k, v):
    """ convert """
    if k in ('price', 'square_meter'):
        if v:
            try:
                return float(v)
            except:
                return None
        else:
            return None
    else:
        return v


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
    # 有时候这个页面会不存在，需要修正为 1，就是总共只有一页，当前为第一页
    current_page = get_number(ur'当前第(\d+)页'.encode(r.encoding), r.content)
    total_page = get_number(ur'总共(\d+)页'.encode(r.encoding), r.content)

    if current_page != page_number + 1:
        logger.warn('Page not correct. current_page: %(current_page)r page_number: %(page_number)r, '
                    'start date: %(start_date)r, end date: %(end_date)r' % locals())

    keys = ('fang_id', 'district', 'location', 'price', 'layout', 'square_meter', 'state', 'agency', 'publish_date')

    session = Session()
    try:
        counter = collections.Counter()
        for element in d('#tab tr').items():
            # skip first column 'index'
            values = [i.text() for i in element('td').items()][1:]
            if values:
                data = dict(zip(keys, values))
                data['_id'] = data['fang_id']
                data['details_url'] = urlparse.urljoin(START_URL, element('td:eq(1) a').attr('href'))
                try:
                    f = Fang(**{k: handle(k, v) for k, v in data.items()})
                    of = session.query(Fang).filter_by(fang_id=data['fang_id']).first()
                    if of:
                        nf = session.merge(f)
                        if session.is_modified(nf):
                            counter['update'] += 1
                            logger.info('Update data. [id=%r diff=%s]' % (nf.fang_id, nf.diff_str()))
                    else:
                        session.add(f)
                        counter['insert'] += 1
                    # commit every time to get error at first place
                    session.commit()
                    logger.debug('Save data: %r' % f)
                except sqlalchemy.exc.SQLAlchemyError:
                    logger.warn('Failed to save data. [exception=%r]' % traceback.format_exc())
                    counter['error'] += 1
                finally:
                    counter['total'] += 1
            else:
                logger.debug('cannot parse line: %r' % element.html())
        logger.info('start date: %(start_date)r, end date: %(end_date)r, '
                    'page: %(current_page)r, counter: %(counter)r' % locals())
    except KeyboardInterrupt:
        raise
    except:
        session.rollback()
        exc = traceback.format_exc()
        logger.warn('rollback. start date: %(start_date)r, end date: %(end_date)r, '
                    'page: %(current_page)r, exception: %(exc)s' % locals())
    finally:
        session.close()
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
                        required=False,
                        type=valid_date)
    parser.add_argument('-e', "--end_date",
                        help="The End Date - format YYYY-MM-DD ",
                        required=False,
                        type=valid_date)
    args = parser.parse_args()
    logger.info('args: %r' % args)

    today = datetime.datetime.combine(datetime.datetime.today(), datetime.time())

    start_date = args.start_date if args.start_date else today
    end_date = args.end_date if args.end_date else start_date
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
