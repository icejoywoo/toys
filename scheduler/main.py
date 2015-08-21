#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import pytz
import model
import datetime

from multiprocessing import Queue, Process, Lock 

#多进程数目
PROCESS_NUM = 40 

def inputQ(q, data):
    q.put(data)

def outputQ(q, lock):
    lock.acquire() 
    try:
        return q.get(timeout=10)
    except Exception, e:
        #model.Log.info('Queue time out %s' % str(e))
        return None
    finally:
        lock.release()
        

#tz = pytz.timezone('Asia/Shanghai')

class RerunProcess(Process):
    """
    重跑表数据读取进程 
    """

    def __init__(self, queue):
        super(RerunProcess, self).__init__()
        self.queue = queue
        #取从跑列表条数
        self.limit = 50 

    #覆盖run方法
    def run(self):
        ReObj = model.rerunModel()
        HsObj = model.historyModel()
        second = time.time()
        while True:
            #检查退出标记
            myexit(self.queue, 2)
            #断开数据库连接
            second = clearFun(ReObj, second)
            if not self.__timer():
                time.sleep(90)
                print 'sleep!'
                continue
            
            rl = ReObj.getList(self.limit)
            if rl:
                l = self.__rerunFun(rl)
            else:
                time.sleep(90)
                continue

            if not l:
                time.sleep(90)
                continue

            for i in l:
                
                if i.get('cycle') == 'hour':
                    ttable = "ns_crm.task_running_history_hour" 
                else:
                    ttable = HsObj.table
                #把rerun记录表改为init已经初始化的状态，防止重复无效初始化工作
                #ReObj.updateFun(i.get('rid', None), status='init')
                #检查依赖
                if not HsObj.checkRely(i.get('rely'), i.get('ctime'), ttable):
                    model.Log.debug('task key %s no ready: %s' % (i.get('key'), i.get('rely')))
                    continue
                #put queue
                inputQ(self.queue, i)
                #更新重跑列表的状态。
                ReObj.uprunFun(i.get('rid'))
                ttype = HsObj.iif(i.get('hour') is None, 'day', 'hour')

                #修改Task status
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                HsObj.updateByKey(i.get('key'), i.get('ctime'), [('status', 'running'), ('begin_time', now)], ttype)
            #sys.exit('in over')
            time.sleep(90)
            

    def __rerunFun(self, rl):
        """
        #重跑记录表，读Task信息放到执行队列
        """
        if not isinstance(rl, list) or not rl:
            return False

        HsObj = model.historyModel()
        ThObj = model.thourModel()
        #HsObj.reinitFun(rl)

        #nomal/hour
        initnl = []
        inithl = []
        idhl = []
        idnl = []
        
        #循环初始化重跑任务
        for i in rl:
            #Todo 表字段是带时区的。暂时当前时间加时区，避免日期init错误。
            #date = i.get('task_date') + datetime.timedelta(hours=8)
            if not i:
                continue

            date = i.get('task_date')
            if HsObj.initTaskByKey(i.get('task_key'), date, i.get('type')):
                if i.get('type') == 'hour':
                    idhl.append(i.get('id', 0))
                    inithl.append((i.get('task_key'), date.strftime("%Y-%m-%d %H:00:00")))
                else:
                    initnl.append((i.get('task_key'), date.strftime("%Y%m%d")))
                    idnl.append(i.get('id', 0))

        print initnl
        print inithl
        print idnl
        print idhl
        #返还刚init的历史任务，进行任务重跑，添加rerunId，用以更新rerun表
        time.sleep(2)
        nl = []
        if initnl:
            nl = HsObj.getByInit(initnl)
        if nl:
            for i in range(0, len(idnl)):
                nl[i]['rid'] = idnl[i]
                nl[i]['cycle'] = 'day' 

        #小时重跑任务
        hl = []
        if inithl:
            hl = ThObj.getByInit(inithl)
        if hl:
            for i in range(0, len(idhl)):
                hl[i]['rid'] = idhl[i]
                hl[i]['cycle'] = 'hour' 

        return nl + hl
    
    def __timer(self):
        """进程在固定时间段不执行任务"""
        hour = int(time.strftime('%H', time.localtime(time.time())))
        if 0 < hour < 8:
            return False
        return True


#HourProcess()
class HourProcess(Process):
    """
    正常调度进程，负责running histroy hour表数据读取。
    """

    def __init__(self, queue, date=None):
        super(HourProcess, self).__init__()
        self.date = date
        self.queue = queue
        self.limit = 5 
        #当前允许执行的最大数目
        self.runningNum = 30 

    #覆盖run方法
    def run(self):
        ThObj = model.thourModel()
        HsObj = model.historyModel()

        #往前执行的时间间隔，保证已有依赖当前任务可执行
        hourSpan = [3, 12, 36]

        ts = time.time()
        hs = time.time()
        while True:
            #检查退出标记
            myexit(self.queue, 3)
            #断开数据库连接
            ts = clearFun(ThObj, ts)
            hs = clearFun(ThObj, hs)

            for hhour in hourSpan:
                num = int(ThObj.getRunningNum(hhour).get('num'))
                print num
                if num > self.runningNum:
                    time.sleep(60)
                    continue
                
                l = ThObj.getNowWaitingTasks(hour=hhour)
                #判断l，为空sleep
                if not l:
                    time.sleep(90)
                    continue
                for i in l:
                    time.sleep(1)
                    #检查依赖
                    if not HsObj.checkRely(i.get('rely'), i.get('ctime'), ThObj.table):
                        model.Log.debug('hour task key: %s , rely no ready: %s' % (i.get('key'), i.get('rely')))
                        #print 'rely no ready'
                        continue                
                    #put queue
                    inputQ(self.queue, i)

                    #修改Task status
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                    ThObj.updateById(i.get('id'), [('status', 'running'), ('begin_time', now)])
                time.sleep(10)
                #sys.exit('in over')
            time.sleep(90)
            


class RoutineProcess(Process):
    """
    正常调度进程，负责running histroy表数据读取。
    """

    def __init__(self, queue, date=None):
        super(RoutineProcess, self).__init__()
        self.date = date
        self.queue = queue
        self.limit = 150

    #覆盖run方法
    def run(self):
        HsObj = model.historyModel()
        second = time.time()
        while True:
            #检查退出标记
            myexit(self.queue, 1)
            #断开数据库连接
            second = clearFun(HsObj, second)

            if not self.date:
                date = time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 86400))
            else:
                date = self.date
            
            model.Log.debug('date is: %s' % date)
            num_run = HsObj.getRunningNum(date).get('num', 0)
            #判断running状态的任务数，任务超过50，就不添加任务，便于高优先级的任务优先执行
            model.Log.debug('running num is: %s' % num_run)
            if num_run > 50:
                time.sleep(180)
                continue
				
            num = HsObj.getWaitingNum(date).get('num', 0)
            model.Log.debug('num is: %s' % num)

            if num > 0:
                l = HsObj.getWaitingTasks(date, self.limit)
            else:
                time.sleep(90)
                continue
            #判断l，为空sleep
            if not l:
                time.sleep(90)
                continue
            for i in l:
                
                if not HsObj.checkRely(i.get('rely'), i.get('ctime')):
                    model.Log.debug('%s task rely no ready,rely is: %s' % (i.get('key'),i.get('rely')))
                    continue                
                #put queue
                inputQ(self.queue, i)

                #修改Task status
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                HsObj.updateByKey(i.get('key'), i.get('ctime'), [('status', 'running'), ('begin_time', now)],'day')
            #sys.exit('in over')
            time.sleep(20)
            
    #进程在固定时间段不执行任务
    def __timer(self):
        hour = int(time.strftime('%H',time.localtime(time.time())))
        if 0 < hour < 2:
            return False
        return True



class workProcess(Process):
    """
    docstring for workProcess
    #干活进程
    """
    def __init__(self, queue, lock):
        super(workProcess, self).__init__()
        self.queue = queue
        self.lock  = lock

        
    def run(self):
        HsObj = model.historyModel()
        ReObj = model.rerunModel()
        sh = time.time()
        sr = time.time()

        while True:
            #Q队列为空sleep 20s
            rs = outputQ(self.queue, self.lock)
            sh = clearFun(HsObj, sh)
            sr = clearFun(ReObj, sr)
            if not rs:
                time.sleep(20)
                continue

            if rs == '__exit__':
                inputQ(self.queue, '__exit__')
                model.Log.debug('work process over pid %d' % os.getpid())
                sys.exit(0)


            print rs.get('key')
            print rs.get('ctime')

            HsObj.runTask(rs)
            
            #更新重跑表状态，非重跑数据没有rid字段
            ReObj.updateFun(rs.get('rid', 0))

            time.sleep(5)

            #Todo测试退出
    
            #inputQ(self.queue, '__exit__')
    
        
def checkFun(pNum=1):
    """
    #执行检查当前进程数目
    """
    cmd = "ps aux | grep 'python main.py' | grep -v 'grep' | wc -l"
    num = int(os.popen(cmd).readlines()[0])
    if (num > pNum):
        sys.exit('main process has running!')

def clearFun(Obj, sec):
    """
    定时关闭数据库连接，避免OperationalError: (2013, "Lost connection to MySQL server at 'reading authorization packet', system error: 104")
    """
    if (int(time.time()) - int(sec)) > 1800:
        try:
            Obj.close()
            return time.time()
        except Exception as e:
            return time.time()
    return sec


def myexit(Q, sign=1):
    """
    #主动进程结束标记
    signal下面存在exit文件，则退出
    """
    signal = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'signal/s' + str(sign)) 

    if os.path.exists(signal):
        os.remove(signal)
        inputQ(Q, '__exit__')
        sys.exit(0)
    else:
        pass
    return True


def daemonize(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile=None, startmsg = 'started with pid %s' ):
    '''
    This forks the current process into a daemon
    '''
    # flush io
    sys.stdout.flush()
    sys.stderr.flush()
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)       
    # Decouple from parent environment.
    os.chdir("/home/work")
    os.umask(0)
    os.setsid()
    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Open file descriptors and print start message
    if not stderr: 
        stderr = stdout
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)  #unbuffered
        pid = str(os.getpid())
        sys.stderr.write("\n%s\n" % startmsg % pid)
        sys.stderr.flush()
    if pidfile:
        file(pidfile,'w+').write("%s\n" % pid)
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def parseTime():
    #date = time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 86400))
    return None

def startFun():
    #开始执行清理历史状态
    ThObj = model.thourModel()
    print ThObj.rebootDo()

def main():
    if (len(sys.argv) >=2 and (sys.argv[1] == '-d' or sys.argv[1] == '-daemon')):
        '''进入后台运行'''
        daemonize(stdout=os.path.join(os.path.split(os.path.realpath(__file__))[0], 'deamon.log'))
    #防止重复起脚本
    checkFun()
    #开始执行清理旧状态
    startFun()

    q = Queue()
    #读取需要处理的Task
    dl = []
    dl.append(RerunProcess(q))
    dl.append(HourProcess(q))
    dl.append(RoutineProcess(q))

    #wait List
    joinList = []

    for i in dl:
        i.daemon = True
        i.start()
        joinList.append(i)

    l = Lock()
    
    for i in range(PROCESS_NUM):
         w = workProcess(q, l)
         w.start()
         joinList.append(w)

    for p in joinList:
        p.join()

if __name__ == '__main__':
    main()
