#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runImportBeaconLog.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import sys
import time
import json
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')


import downlog
import genDataFrame
import logAnalyzer
import common as cm
from beaconCount import BeaconCount

import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import datetime


from appkeylist import APPKEY_FILENAME

isCSVwrite = True
isLogDown = True
# Log configureation
servertype = 's3'
frameSize = -1


# get appkey information
appKeyFilename = APPKEY_FILENAME
appKeyfile =  open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()
logdate='20170330'
device_amount=500000    # the number of device
period=13               # the number of rcvd trials

# beacon 로그 처리
logtype = 'beacon'
loadingType ='json'
if isLogDown:
    downBeaconLogDownWorker = downlog.LogDownloader()
    downBeaconLogDownWorker.setLogInfo(logdate, logtype, servertype)
    downBeaconLogDownWorker.downLogRecord()

# Beacon Log in json format to dataframe format
dailybeaconlogworker = genDataFrame.DailyLogWorker()
dailybeaconlogworker.init(logtype, logdate, appKey)
dailybeaconlogworker.get_log_files(loadingType)

#data frame generation
if len(dailybeaconlogworker.mFileNameList) > 0:
    beaconLogDailyDataFrame = dailybeaconlogworker.getDailyDataFrame(-1)
    beaconLogDailyDataFrame.sort_values(by='deviceTime')



if isCSVwrite:
    if not (beaconLogDailyDataFrame.empty):
        BEACONLOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
                                                     '/' + logdate + '_' \
                                                     + logtype + 'Log_' \
                                                     + 'DailyDataFrame' +'.csv'
        beaconLogDailyDataFrame.to_csv(BEACONLOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
        print '# [runDailyLogAnalysis] CSV write done! @ %s' % BEACONLOG_DATAFRAME_CSV_FILENAME


BeaconCount(logdate, device_amount, period, appKey).slack_message_report()

