#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: test_developedCodes.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import sys
import time
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')



import downlog
import genDataFrame
import logAnalyzer
import common as cm

import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as matplot


IsCoreLog = False
IsBeaconLog = True


IsCLiP = False
IsCashSlide = True

# Log configureation
servertype = 's3'
frameSize = -1 # including all records
phoneModel = cm.ALL_TYPE_OF_PHONES

# log profiles
if IsCashSlide:
    # 캐시 슬라이드
    appname = '캐시슬라이드'
    appkey = '5e228d8d-c869-437c-ae70-8dd87b089f64'
    currdate = '20170326'
elif IsCLiP:
    # CLiP
    appname = 'CLiP'
    appkey = '6227368d-7a59-4805-a110-24b23e8c87b3'
    currdate = '20170309'


# core 로그 처리
if IsCoreLog == True:
    logtype = 'core'
    downCoreLogWorker = downlog.LogDownloader()
    downCoreLogWorker.setLogInfo(currdate,logtype,servertype)
    # downCoreLogWorker.downLogRecord()


    dailycorelogworker = genDataFrame.DailyLogWorker()
    dailycorelogworker.init(logtype,currdate,appkey)
    dailycorelogworker.makeDailyLogfileList()
    dailycorelogworker.nextDailyLogFile()

    # Data loading
    t =time.time()
    dailycorelogworker.loadDailyLog('grep')
    elapsed = time.time() - t
    print '# [runDailyLogAnalysis] Data loading time = %s' % elapsed
    # data framing

    if len(dailycorelogworker.mFileNameList) > 0:
        # Data parsing
        t =time.time()
        coreLogDailyDataFrame = dailycorelogworker.getDailyDataFrame(frameSize)
        # coreLogDailyDataFrame.sort_values(by='deviceTime')
        coreLogDailyDataFrame_CRCPASS = coreLogDailyDataFrame[coreLogDailyDataFrame['isCRCPass'] == True]
        coreLogDailyDataFrame_EDPASS = coreLogDailyDataFrame[coreLogDailyDataFrame['isEnergy'] == True]
        elapsed = time.time() - t
        print '# [runDailyLogAnalysis] Data parsing time = %s' % elapsed

       ## Data analysis
        dailyLogAnalyzer = logAnalyzer.DailyLogAnalysisWorker()
        t = time.time()
        dailyLogAnalyzer.setDataFrame(coreLogDailyDataFrame)

        while dailyLogAnalyzer.nextPhoneModel():
            dailyLogAnalyzer.updateCurrPhoneModelResult()
            dailyLogAnalyzer.getCurrPhoneModelDataFrame()

        dailyLogAnalyzer.updateAvgMeasureResult()
        dailyLogAnalyzer.getFalseAlarmEvent()
        dailyLogAnalyzer.getDailyMeasureDataFrame()
        # measureDataFrame = dailyLogAnalyzer.getDailyMeasureDataFrame()

        # dailyLogAnalyzer.updateResult()

        elapsed = time.time() - t
        print  '# [runDailyLogAnalysis] Data analysis time = %s\n' % elapsed


if IsBeaconLog == True:
    logtype = 'beacon'
    # beacon 로그 처리
    downBeaconLogWorker = downlog.LogDownloader()
    downBeaconLogWorker.setLogInfo(currdate,logtype,servertype)
    # downBeaconLogWorker.downLogRecord()

    dailybeaconlogworker = genDataFrame.DailyLogWorker()
    dailybeaconlogworker.init(logtype,currdate,appkey)
    dailybeaconlogworker.makeDailyLogfileList()
    dailybeaconlogworker.nextDailyLogFile()

    dailybeaconlogworker.loadDailyLog('json')

    # data frame generation
    if len(dailybeaconlogworker.mFileNameList) > 0:
        beaconLogDailyDataFrame = dailybeaconlogworker.getDailyDataFrame(-1)
        beaconLogDailyDataFrame.sort_values(by='deviceTime')
        beaconLogDailyDataFrame.to_csv(currdate+'.csv', encoding='utf-8')

