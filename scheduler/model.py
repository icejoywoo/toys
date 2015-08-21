#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import urllib 
import MySQLdb
import urllib2
#import DBUtils
import logging
import datetime
import commands
import traceback
import subprocess

from libs import torndb
from libs import utils 

logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
Log = logging.getLogger('model')

#使用装饰器(decorator),  单例 
def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton


class baseModel(object):
    """docstring for baseModel
    基类初始化数据库链接
    """
    def __init__(self):
        super(baseModel, self).__init__()
        try:
            c = __import__('config')
            c = c.dbConfig
        except:
            sys.exit('check import db config') 
        self.c = c
        #self.db = torndb.Connection(c['host'], 'ns_crm', c['user'], c['passwd'])
        self.db = None
        #邮件发送人
        self.sendTo = ['zhaihuixin@baidu.com']

    def conn(self):
        """
        mysql连接
        """
        try:
            Log.debug('Connection MySQL')
            if self.db == None:
                self.db = torndb.Connection(self.c['host'], 'ns_crm', self.c['user'], self.c['passwd'])
                '''避免DataError: (1406, "Data too long for column'''
                self.db.execute("SET NAMES UTF8")  # 去掉
            return self.db
        except Exception, e:
            Log.debug(traceback.format_exc())
            try:
                self.db = torndb.Connection(self.c['host'], 'ns_crm', self.c['user'], self.c['passwd'])
                self.db.execute("SET NAMES UTF8")
                return self.db
            except Exception, e:
                Log.error(traceback.format_exc())
                time.sleep(20)
    
    def close(self):
        """
        关闭数据库连接
        """
        if self.db is None:
            return True
        try:
            self.db.close()
        except Exception, e:
            Log.debug(traceback.format_exc())

@singleton
class historyModel(baseModel):
    """
    docstring for taskModel
    执行历史操作model类
    """

    #Hive客户端
    hive = '/home/work/hive-2.3.2/bin/hive'

    #匹配log日志记录
    logSed = "sed -n  '/Total MapReduce CPU Time Spent/,/Time taken:/p' <file> | sed -e '1,2d' | sed -e '$ d'"
    logSedPatch = "sed -n  '/Hive history file=/,/Fetched:/p' <file> | sed -e '1,2d' | sed -e '$ d'"

    #记录Hive logs路径
    logPath = '/home/work/crontab/scheduler/result/'

    


    def __init__(self):
        baseModel.__init__(self)
        #表名称
        self.table = 'ns_crm.task_running_history'

        self.hosts = "'vn.hao123.com', 'th.hao123.com', 'tw.hao123.com','br.hao123.com','ar.hao123.com','jp.hao123.com','sa.hao123.com','ae.hao123.com','id.hao123.com','ma.hao123.com'"

        #通知crm更新接口
        self.notifyUrl = 'http://yf-mp3-melody-cal00.yf01.baidu.com:8081/load-data-record'
        self.refreshUrl = 'http://crm.baidu.com/api/job/loadDataRecord?_product_line_=HABO&_secret_key_=987654321&refresh=true'

   
    def getWaitingNum(self, date):
        """
        全部切换TODO以后放弃retry状态
        """
        sql = "select count(*) as num from %s where ctime='%s' and (status='waiting'  or status='retry') " % (self.table, date)
        return baseModel().conn().get(sql)

    def getRunningNum(self, date):
        """
        查看running状态的任务
        """
        sql = "select count(*) as num from %s where ctime='%s' and status='running' " % (self.table, date)
        return baseModel().conn().get(sql)

    
    def getWaitingTasks(self, date, limit=10):
        """
        #获取waitina任务
        """
        sql = "(select * from %s where ctime = '%s' and (status = 'waiting' or status='retry') and product='mbrowser' order by level desc limit 30) union all (select * from %s where ctime = '%s' and (status = 'waiting'  or status='retry') and product='hiclub' order by level desc limit 30) union all (select * from %s where ctime = '%s' and (status = 'waiting'  or status='retry') and product='mobileapp' order by level desc limit 30) union all (select * from %s where ctime = '%s' and (status = 'waiting'  or status='retry') and product='hao123' order by level desc limit 60) union all (select * from %s where ctime = '%s' and (status = 'waiting'  or status='retry') and product not in('hao123','mbrowser','mobileapp','hiclub') order by level desc limit 20)" % (self.table, date, self.table, date, self.table, date, self.table, date, self.table, date)
        return baseModel().conn().query(sql)


    def updateByKey(self, key, date, ulist, ttype='hour'):
        """
        更新history状态
        ulist [(key,val)]
        """
        l = []
        for v in ulist:
            l.append("`%s`='%s'" % v)

        if ttype == 'hour':
            table = thourModel().table
        else:
            table = self.table
        sql = "update %s set %s ,runtimes = runtimes + 1 where `key` = '%s' and ctime = '%s'" % (table, ','.join(l), key, date)
        print sql
        return baseModel().conn().execute(sql)

    
    def checkRely(self, keys, date, table=None):
        """
        #检查当前任务前置依赖
        """
        keys = keys.strip()
        if not keys:
            return True

        if table is None:
            table = self.table 
        #排重
        keyList = list(set(keys.split(',')))
        keyIn = "('" + "','".join(keyList) + "')"
        sql = "select status from %s where ctime = '%s' and `key` in %s" % (table, date, keyIn)
        l = baseModel().conn().query(sql)
        
        if not l:
            return False
        #如果结果条数和key数目不一致，也返回False
        if len(keyList) != len(l):
            return False

        for d in l:
            if d.get('status') != 'finished':
                return False
        #Sql = "select status from task_running_history where ctime='$this->taskTime' and `key`='$value'";
        return True

    def getByInit(self, ilist):
        """
        #####################################
        Just for rerun task get
        """
        where = []
        for s in ilist:
            where.append("(`key` = '%s' and ctime = '%s')" % s)

        if not where:
            return False
        sql = "select * from %s where %s" % (self.table, ' or '.join(where))
        return baseModel().conn().query(sql)

    
    def initTaskByKey(self, key, date, ttype="hour", task=None, isRerun=True):
        """
        初始化当前任务
        @params task任务内容
        @params isRerun 是否是重跑，sql不同
        """
        if not key:
            return False

        if task is None:
            t = libraryModel().getByKey(key, ttype)
        else:
            t = task
        if not t:
            return False


        start = self.iif(isRerun == True, 'replace', 'insert')

        hour = date.strftime('%H')
        hql = MySQLdb.escape_string(self.__replaceHour(self.__replaceDate(self.__replaceHosts(t.get('hql'), t.get('key')), date), hour))
        #hql = MySQLdb.escape_string(self.__replaceMonth(self.__replaceHour(self.__replaceDate(self.__replaceHosts(t.get('hql'), t.get('key')), date), hour),date))
        ctime_hour = date.strftime('%Y-%m-%d %H:00:00')
        ctime = date.strftime('%Y-%m-%d 00:00:00')
        com = t.get('check_command') + 'init newPy'

        params_hour = [ctime_hour, key, t.get('level'), t.get('output'), hql, t.get('table'), t.get('source'), t.get('db'), 'waiting', t.get('product'), t.get('rely'), t.get('run_command'), com, t.get('author')]
        params = [ctime, key, t.get('level'), t.get('output'), hql, t.get('table'), t.get('source'), t.get('db'), 'waiting', t.get('product'), t.get('rely'), t.get('run_command'), com, t.get('author')]

        if ttype == 'hour':
            params_hour.insert(0, thourModel().table)
            params_hour.insert(2, int(hour))
            sql = start + " into %s(`ctime`,`hour`,`key`,`level`,`output`,`hql`,`table`,`source`,`db`,`status`,`product`,`rely`,`run_command`,`check_command`,`author`) values ('%s','%d','%s','%d','%s',\"%s\",'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(params_hour)
        else:
            params.insert(0, self.table)
            sql = start + " into %s(`ctime`,`key`,`level`,`output`,`hql`,`table`,`source`,`db`,`status`,`product`,`rely`,`run_command`,`check_command`,`author`) values ('%s','%s','%d','%s',\"%s\",'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(params)

        print sql
        try:
            rs = baseModel().conn().execute(sql)
            print ['init task', rs]
            return True
        except Exception, e:
            Log.debug(traceback.format_exc())
            return False

    def __replaceHosts(self, hql, key):
        '''替换Hql的国家'''
        '''游戏二级页添加fungame统计'''
        fungamel = ['daily_level2', 'channel_pageid_modId_click_statistic', 'level2_channel_pageId', 'globalhao123_pageId_mod_sot', 'globalhao123_guide_flow', 'level2_channel_inside_statistic', 'tn_level2_daily_report', 'tn_level2_month_report', 'channel_sort_click_statistic']
        if key in fungamel:
            return hql.replace('<hosts>', self.hosts + ",'www.fungame.com.br'")
        else:
            return hql.replace('<hosts>', self.hosts)

    def __replaceDate(self, hql, date):
        """
        替换hql里面的<date>和<hosts>变量
        """
        dates = date.strftime('%Y%m%d')
        day = date.strftime('%Y-%m-%d')
        #%%转义
        hql = hql.replace("<date>", dates).replace('%', '%%')
        hql = hql.replace("<day>",day)
        #print hql
        #正则匹配到date-n的数据
        Re = re.compile(r'<date\s*-\s*(\d+)>')
        l  = Re.findall(hql)
        if not l:
            return hql

        l = map(lambda x: int(x), l)
        for n in l:
            stamp = int(time.mktime(time.strptime(dates, '%Y%m%d'))) - 86400 * n
            
            match = Re.search(hql)
            if not match:
                continue

            #替换<date-n>为具体时间。时区问题，用localtime转date，注意最后参数1！！
            sdate = time.strftime("%Y%m%d", time.localtime(stamp))
            hql = hql.replace(match.group(), str(sdate), 1)

        return hql

    def __replaceMonth(self, hql, date):
        """
        替换hql中的month变量
        """
        date=date.strftime('%Y%m01')
        hql = hql.replace("<month>", date).replace('%', '%%')
		
		#print hql
        #正则匹配到month-n的数据
        Re = re.compile(r'<month\s*-\s*(\d+)>')
        l  = Re.findall(hql)
        if not l:
            return hql
		
        l = map(lambda x: int(x), l)
        for n in l:
            date_from = datetime.datetime(date.year, date.month-int(n), 1, 0, 0, 0).strftime('%Y%m01')
            match = Re.search(hql)
            if not match:
                continue
				
            hql = hql.replace(match.group(), str(date_from), 1)

    def __replaceHour(self, hql, hour):
        return hql.replace("<hour>", hour)
        
    def runTask(self, d=None):
        """
        #执行task任务入库
        """
        #switch方法
        opFun = {
            'hive_to_mysql': self.__hive2MysqlFun,
            'hive': self.__hiveFun,
            'shell': self.__shellFun,
            'mysql': self.__mysqlFun,
            'inmysql': self.__mysqlFun,
            'download': self.__downloadFun,
            'mysql_to_hive': self.__mysql2HiveFun
        }
        
        #time.sleep(2)
        if not isinstance(d, dict):
            return False

        #检查日志目录，创建
        date = d.get('ctime').strftime("%Y%m%d")
        self.__mkdirLog(date)

        r = opFun.get(d.get('source'))(d)
        if not r:
            #查询失败发邮件
            title = "Query task '%s' Failure" % d.get('key')
            body = "Task %s Failure, please check the log for details. http://query.hao123.com/task/history/index/?date=%s"
            body = body % (d.get('key'), date)
            utils.sendmail('mengrui@baidu.com', d.get('author'), title, body)
        return True

    def __mysqlFun(self, d):
        """执行mysql任务"""
        ttype = self.iif(d.get('hour') is None, 'day', 'hour')
        self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'running')], ttype)

        #TODO 初始化时候mysql的处理配合，在用init.py后
        sql = d.get('hql').replace('"', '\\"').replace('%', '%%')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        try:
            if baseModel().conn().execute(sql) == 0:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'finished'), ('finished_time', now)], ttype)
                return True
            else:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'failure'), ('finished_time', now)], ttype)
                return False
        except Exception as e:
            self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'failure'), ('finished_time', now)], ttype)
            title = "Query task '%s' Error" % d.get('key')
            utils.sendmail('mengrui@baidu.com', d.get('author'), title, str(e))
            return False

        return True

    def __hive2MysqlFun(self, d):
        """
        #发送Hql到hive客户端
        """
        hql = "use %s; %s" % (d.get('db'), d.get('hql').replace('[\r\n]+', '\n ').replace('"', '\\"'))
        print hql

        cmd = "%s -e \"%s\"" % (historyModel().hive, hql)
        date = d.get('ctime').strftime("%Y%m%d")

        #任务没有hour字段取时候返回None，则是天任务
        log = self.__logFile(d.get('key'), date, d.get('hour'))
        #执行hive任务
        rs = self.__cmdRun(cmd, log, log)
        if rs == 0:
            self.__notifyCrm(d.get('table'), date)
        print rs

        return self.__taskGc(rs, d)
        
    
    def __logFile(self, key, date, hour=None):
        """返回log文件路径"""
        if hour is None:
            return os.path.join(historyModel().logPath, date, key)
        else:
            return os.path.join(historyModel().logPath, date, "%s_%d" % (key, int(hour)))


    def __hiveFun(self, d):
        """执行hive任务"""
        hql = "use %s; %s" % (d.get('db'), d.get('hql').replace('\t', '  ').replace('\r\n', '\n').replace('"', '\\"'))

        cmd = "%s -e \"%s\"" % (historyModel().hive, hql)
        date = d.get('ctime').strftime("%Y%m%d")

        log = self.__logFile(d.get('key'), date, d.get('hour'))
        rs = self.__cmdRun(cmd, log, log)
        print rs

        return self.__taskGc(rs, d, 'hive')

    def __downloadFun(self, d):
        """执行数据下载任务"""
        Log.debug('download' + d.get('key'))
        hql = "use %s; %s" % (d.get('db'), d.get('hql').replace('\t', '  ').replace('\r\n', '\n').replace('"', '\\"'))
        cmd = "%s -e \"%s\"" % (historyModel().hive, hql)
        date = d.get('ctime').strftime("%Y%m%d")
        log = self.__logFile(d.get('key'), date, d.get('hour'))
		
        #构建下载数据保存的结果文件
        l = [log,'_',date,'.txt']
        data = ''
        data = ''.join(l)
        rs = self.__cmdRunDownload(cmd, data, log)
        Log.debug('download' + d.get('key'))
        print rs 
        cmd = "gzip -f %s" % (data)
        subprocess.check_call(cmd,shell=True)
        time.sleep(10)
        subprocess.check_call(['scp', data+'.gz', 'work@hkg02-gpm-datag02.hkg02.baidu.com:/home/work/wwwroot/query_bingo/web/resource/.log/download'])

        return self.__taskGc(rs, d, 'download')
		
		
    def __mysql2HiveFun(self,d):
        """ִÐmysqlµ½hiveµÄýäÎ"""
        Log.debug('mysql2HiveFun' + d.get('key'))
        date = d.get('ctime').strftime("%Y%m%d")
        log = self.__logFile(d.get('key'), date, d.get('hour'))
        mysqlcmd = "/home/work/local/mysql/bin/mysql -h hkg02-gpm-datag01.hkg02.baidu.com -u datagroup -pdatagrouppass %s -e \"select * from %s;\" --skip-column-names > %s 2>&1" % (d.get('output'),d.get('table'),log)
        subprocess.check_call(mysqlcmd,shell=True)
                         
        hql = "use %s; load DATA LOCAL inpath \'%s\' OVERWRITE INTO TABLE %s;" % (d.get('db'), log, d.get('table'))
        cmd = "%s -e \"%s\"" % (historyModel().hive, hql)
        logFile = log+'.log'
        rs = self.__cmdRun(cmd,logFile,logFile)
        print rs
        return self.__taskGc(rs, d, 'mysql_to_hive') 


    def __taskGc(self, r, d, t='hive2mysql'):
        """Task任务收尾工作，更新状态"""
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        ttype = self.iif(d.get('hour') is None, 'day', 'hour')
        print ttype
        if r == 0:
            if t == 'hive2mysql':
                if self.loadFile2Mysql(d.get('table'), d.get('output'), d.get('key'), d.get('ctime'), ttype):
                    self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'finished'), ('finished_time', now)], ttype)
                else:
                    self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'empty_result'), ('finished_time', now)], ttype)
            else:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'finished'), ('finished_time', now)], ttype)

            return True
        elif r is None:
            Log.debug(d.get('key') + ' Maybe time out!!')
            Log.debug(r)
        else:
            #任务其它状况
            Log.debug(d.get('key') + ' please check the task %s' % str(r))

        self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'failure'), ('finished_time', now)], ttype)
        return False


    def __notifyCrm(self, table, date):
        """通知crm平台"""
        m = re.match('^ha_(.*?)', table)
        if not m:
            return True
        try:
            url = '%s?table_name=%s&datatime=%s' % (self.notifyUrl, table, date)

            n = urllib2.Request(url)
            rp = urllib2.urlopen(n)
            html = rp.read()
            print html
            
            url = '%s?table_name=%s&datatime=%s' % (self.refreshUrl, table, date)
            
            r = urllib2.Request(url)
            rp = urllib2.urlopen(r)
            print rp.read()
        except Exception as e:
            Log.debug(e)
            return False



    def __shellFun(self, d):
        '''执行shell类型的任务'''
        ttype = self.iif(d.get('hour') is None, 'day', 'hour')
        if (ttype == 'hour'):
            cmd = '%s \'%s\'' % (d.get('run_command'), d.get('ctime').strftime("%Y-%m-%d %H:%M:%S"))
            print cmd
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            status, output = commands.getstatusoutput(cmd)
            print now + output     
            if (output == 'Ready'):
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'finished'), ('finished_time', now)], ttype)
                return True
            if status == 0:
                time.sleep(120)
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'waiting')], ttype)
                return True
            else:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'failure'), ('finished_time', now)], ttype)
                return False
	
        else:		
            cmd = '%s %s' % (d.get('run_command'), d.get('ctime').strftime("%Y%m%d"))
            print cmd
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            status, output = commands.getstatusoutput(cmd)
            if (output == 'notReady'):
                time.sleep(300)
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'waiting')], ttype)
                return True
            if status == 0:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'finished'), ('finished_time', now)], ttype)
                return True
            else:
                self.updateByKey(d.get('key'), d.get('ctime'), [('status', 'failure'), ('finished_time', now)], ttype)
                return False
        
    
    def __mkdirLog(self, date):
        """
        #创建日志日期目录
        """
        path = os.path.join(historyModel().logPath, date)

        if os.path.exists(path):
            return True

        os.makedirs(path)


    def loadFile2Mysql(self, table, output, key, ctime, type='day'):
        """
        导Log日志到msyql数据库
        """
        date = ctime.strftime("%Y%m%d")
        #date = ctime.replace("-","")
        #date = time.strftime("%Y%m%d",time.strptime(ctime, "%Y-%m-%d"))
        if (type == 'hour'):
            hour = ctime.strftime("%H")
            ctime = ctime.strftime("%Y-%m-%d %H:00:00")
            log = self.__logFile(key, date, hour)
        else:
            log = self.__logFile(key, date)
            ctime = date

        lines = int(os.popen('wc -l ' + log).read().split()[0])
        if lines > 30000:
            utils.sendmail('mengrui@baidu.com', self.sendTo, 'hive log is too big', "Hive log is :%s  at %s \n" % (log, ctime))
            return False


        #sed过滤出hive log数据
        str = subprocess.check_output(historyModel().logSed.replace('<file>', log), shell=True)
        if not str.strip():
            str = subprocess.check_output(historyModel().logSedPatch.replace('<file>', log), shell=True)

        if not str.strip():
            Log.info('sed log file result is empty: %s' % key)
            return False


        outList = output.split(',')
        map(lambda x: x.strip(), outList)

        cleanList = []
        strl = str.split("\n")
        for line in strl:
            if not line:
                continue
            ll = line.split("\t")
            if len(ll) != len(outList):
                Log.info('colums num not match: %s **** %s' % (line, key))
                continue
            #进行字符串的urldecode
            ll = map(urllib.unquote, ll)

            if not self.__validContent(ll, outList):
                print ll
                print outList
                continue

            ll.insert(0, ctime)
            cleanList.append(ll)


        if len(cleanList) == 0:
            Log.info('result is empty: %s' % key)
            return False

        sql = self.__makeInsertSql(table, outList)
        #入库mysql逻辑，分批次入库。按步长分片
        #for z in range(len(cleanList)):
            #cleanList[z] = map(lambda x: self.iif(x == 'NULL', '', x), cleanList[z])

        stepNum = 20
        for ii in xrange(0, len(cleanList), stepNum):
            l = cleanList[ii:ii+stepNum]
            if l:
                try:
                    rs = baseModel().conn().insertmany(sql, l)
                except Exception as e:
                    Log.warning(l)
                    msg = traceback.format_exc()
                    Log.warning(msg)
                    
                    utils.sendmail('mengrui@baidu.com', self.sendTo, 'Insertmany Exception Msg', "Task %s in mysql error at %s \n\n details: %s" % (key, ctime, msg))
            else:
                continue
        return True


    def __validContent(self, recordL, output):
        '''验证数据合法性'''
        fl = ['tn', 'globalhao123_tn', 'refer_from', 'globalhao123_channel']

        #enumerate 
        for i in range(len(output)):
            if output[i].lower() in fl:
                if re.match(r'^[a-zA-Z0-9_\|]+$', recordL[i]) is None:
                    return False
            else:
                continue
        return True

    def iif(self, condition, tp, fp):
        """三目运算函数"""
        return (condition and [tp] or [fp])[0]

    def __makeInsertSql(self, table, outList):
        """
        生成入库sql
        """
        l = []
        for i in outList:
            l.append("%s=VALUES(%s)" % (i, i))
        k = ','.join(l) 
        f = "ctime, `%s`" % "`,`".join(outList) 
        v = ("%s," * (len(outList) + 1))[:-1]
        sql = "insert into %s (%s) values (%s) ON DUPLICATE KEY UPDATE %s" % (table, f, v, k)
        return sql

    def __cmdRun(self, cmd, out=None, err=None, timeout=30800):
        """
        #执行shell脚本，带超时控制，默认超时时间10800秒。
        """
        if out is None:
            out = subprocess.PIPE
        if err is None:
            err = subprocess.PIPE
        #存在历史log，删除
        if os.path.exists(out):
            os.remove(out)

        fd = open(out, 'w')
        sp = subprocess.Popen(cmd, bufsize=2048, stdout=fd, stderr=fd, shell=True)

        currTime = time.time()

        while sp.poll() is None:
            time.sleep(10)
            if int(time.time() - currTime) > timeout:
                Log.warning("Timeout 10800: %s" % cmd)
                utils.sendmail('mengrui@baidu.com', self.sendTo, 'Task running timeout 30800', "Task run timeout, CMD: %s" % cmd)
                try:
                    sp.kill()
                except Exception,e:
                    return None
                return None
                #raise Exception("Timeout 3600: %s" % cmd)

        fd.close()
        if sp.stdin:
            sp.stdin.close()
        if sp.stdout:
            sp.stdout.close()
        if sp.stderr:
            sp.stderr.close()
        try:
            sp.kill()
        except OSError:
            pass
        return sp.returncode

    def __cmdRunDownload(self, cmd, out=None, err=None, timeout=10800):
        """
        #执行shell脚本，带超时控制，默认超时时间10800秒。
        """
        if out is None:
            out = subprocess.PIPE
        if err is None:
            err = subprocess.PIPE
        #存在历史log，删除
        if os.path.exists(out):
            os.remove(out)
        if os.path.exists(err):
            os.remove(err)
			
        fd = open(out, 'w')
        fe = open(err, 'w')
        sp = subprocess.Popen(cmd, bufsize=2048, stdout=fd, stderr=fe, shell=True)

        currTime = time.time()

        while sp.poll() is None:
            time.sleep(10)
            if int(time.time() - currTime) > timeout:
                Log.warning("Timeout 10800: %s" % cmd)
                utils.sendmail('mengrui@baidu.com', self.sendTo, 'Task running timeout 10800', "Task run timeout, CMD: %s" % cmd)
                try:
                    sp.kill()
                except Exception,e:
                    return None
                return None
                #raise Exception("Timeout 3600: %s" % cmd)

        fd.close()
        if sp.stdin:
            sp.stdin.close()
        if sp.stdout:
            sp.stdout.close()
        if sp.stderr:
            sp.stderr.close()
        try:
            sp.kill()
        except OSError:
            pass
        return sp.returncode


@singleton
class libraryModel(baseModel):
    """
    docstring for libraryModel
    task_library库操作逻辑
    """
    def __init__(self,  ):
        #super(libraryModel, self).__init__()
        baseModel.__init__(self)
         

    def getList(self, ttype='hour', page=1, limit=50, status=3):
        """
        获取Task任务
        """
        if page >= 1:
            offset = (page - 1) * limit
        else:
            offset = 0

        if ttype == 'hour':
            sql = "select * from ns_crm.task_library where status=%d and cycle='%s' limit %d, %d" % (status, ttype, offset, limit)
        else:
            sql = "select * from ns_crm.task_library where status=%d and cycle='%s' limit %d, %d" % (status, ttype, offset, limit)
        return baseModel().conn().query(sql)

    def getNum(self, ttype='hour', status=3):
        '''获取任务条数'''
        if ttype == 'hour':
            sql = "select count(*) as num from ns_crm.task_library where cycle = 'hour' and status = %d" % status
        else:
            sql = "select count(*) as num from ns_crm.task_library where cycle != 'hour' and status = %d" % status
        return baseModel().conn().get(sql)


    def getByKey(self, key, ttype='day'):
        """
        根据key获取task内容，因key后来可以重复，加上cycle条件。
        """
        if not key:
            return False
        sql = "select * from ns_crm.task_library where status = 3 and `key` = '%s' and `cycle` = '%s'" % (key, ttype)
        return baseModel().conn().get(sql)


@singleton
class rerunModel(baseModel):
    """docstring for rerunModel
    任务重跑逻辑
    """
    def __init__(self):
        baseModel.__init__(self)
        self.table = 'ns_crm.task_rerun_record'

    def getList(self, limit=10):
        """
        获取需要从跑的任务
        """
        #Todo跑天的数据
        sql = "select * from %s where status = 'waiting' order by id asc limit %d" % (self.table, limit)
        return baseModel().conn().query(sql)

    def uprunFun(self, llist):
        """
        标记任务开始，刚入队列就更新当前状态
        """
        if not llist:
            return False
        l = []
        if str(llist).isdigit():
            l = [llist]
        else:
            for i in llist:
                l.append(i.get('id', 0))

        l = map(str, l)
        id = ','.join(l)
        sql = "update %s set status = 'running' where id in (%s)" % (self.table, id)
        return baseModel().conn().execute(sql)

    def updateFun(self, id, status='finished'):
        """
        设置任务状态，添加初始化状态(init)
        """
        if not id:
            return False
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        sql = "update %s set status = '%s', finished_date = '%s' where id = %d" % (self.table, status, now, id)
        return baseModel().conn().execute(sql)


@singleton
class thourModel(baseModel):
    """task running history hour表数据读取model"""
    def __init__(self):
        self.table = "ns_crm.task_running_history_hour"

    def getNowWaitingTasks(self, date=None, hour=3, limit=50):
        """Y-m-d H:00:00日期格式，！！正常小时调度获取，因任务依赖延迟添加hour值，动态调整task任务范围"""
        if date is None:
            date = time.strftime("%Y-%m-%d %H:00:00", time.localtime(int(time.time()) - 3600 * hour))
        sql = "select * from %s where ctime >= '%s' and status='waiting' order by id asc limit %d" % (self.table, date, limit)
        return baseModel().conn().query(sql)

    def getRunningNum(self, hour=3):
        """获取当前正在运行的数目"""
        ddate = datetime.datetime.now() - datetime.timedelta(hours=hour)
        ttime = ddate.strftime('%Y-%m-%d %H:00:00')
        sql = "select count(*) as num from %s where status='running' and ctime >= '%s'" % (self.table, ttime)
        return baseModel().conn().get(sql)

    def updateById(self, id, ulist):
        """更新history，状态ulist [(key,val)]"""
        l = []
        for v in ulist:
            l.append("`%s`='%s'" % v)

        sql = "update %s set %s where `id` = '%d'" % (self.table, ','.join(l), id)
        return baseModel().conn().execute(sql)

    def getByInit(self, ilist):
        """
        #####################################
        Just for rerun task get
        """
        where = []
        for s in ilist:
            where.append("(`key` = '%s' and ctime = '%s')" % s)

        if not where:
            return False
        sql = "select * from %s where %s" % (self.table, ' or '.join(where))
        print sql
        return baseModel().conn().query(sql)

    def rebootDo(self):
        '''脚本挂掉时候，从启清理数据库记录状态，避免无法再次执行'''
        date = time.strftime("%Y-%m-%d %H:00:00", time.localtime(int(time.time()) - 3600 * 24))
        sql = "update %s set status='waiting' where ctime >= '%s' and status='running'" % (self.table, date)
        return baseModel().conn().execute(sql)

    

