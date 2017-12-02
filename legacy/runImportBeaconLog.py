#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runImportBeaconLog.py
# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import sys
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')


import downlog
import genDataFrame
import common as cm
import intro

import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import datetime


from appkeylist import APPKEY_FILENAME


# script configuration
isCSVwrite = True
isLogDown = False
# Log configureation
servertype = 's3'

# if FrameSize == -1: all take items from the log
frameSize = -1


# intro
intro.intro_ImportBeaconLog()

# get appkey information
appKeyFilename = APPKEY_FILENAME
appKeyfile =  open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()
logdate='20170704'


# beacon 로그 처리
logtype = 'beacon'
if isLogDown:
    downLogWorker = downlog.LogDownloader()
    downLogWorker.setLogInfo(logdate, logtype, servertype)
    downLogWorker.downLogRecord()
    #  --------파일 디렉토리 이동하는 부분 필요 ------%


# Beacon Log in json format to dataframe format
genDataFrameWorker = genDataFrame.DailyLogWorker()
genDataFrameWorker.init(logtype, logdate, appKey)


# Jisoo method
# genDataFrameWorker.get_log_files('json')

# jwkang method
genDataFrameWorker.makeDailyLogfileList()
genDataFrameWorker.nextDailyLogFile()
genDataFrameWorker.loadDailyLog('json')


#data frame generation
if len(genDataFrameWorker.mFileNameList) > 0:
    beaconLogDailyDataFrame = genDataFrameWorker.getDailyDataFrame(-1)
    beaconLogDailyDataFrame.sort_values(by='deviceTime')



if isCSVwrite:
    if not (beaconLogDailyDataFrame.empty):
        BEACONLOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_BEACON_CSV_DIR + \
                                                     '/' + logdate + '_' \
                                                     + logtype + 'Log_' \
                                                     + 'DailyDataFrame' +'.csv'
        beaconLogDailyDataFrame.to_csv(BEACONLOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
        print '# [runDailyLogAnalysis] CSV write done! @ %s' % BEACONLOG_DATAFRAME_CSV_FILENAME

