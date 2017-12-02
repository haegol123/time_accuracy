#-*- coding: utf-8 -*-
#!/usr/bin/python
#------------------------------------------------------------
# filename: runImportDetectLog.py
# written by Jaewook Kang @ July 2017
#------------------------------------------------------------
import sys
from os import getcwd
sys.path.insert(0,getcwd()+'/python_codes')

import downlog
import genDataFrame
import common as cm
from datetime import datetime
import intro
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

import argparse
import subprocess
from appkeylist import APPKEY_FILENAME


isCSVwrite  = True
isLogDown   = False

# Log config
logtype = 'detect'

# if FrameSize == -1, take all items from the log
frameSize = -1

# intro
intro.intro_ImportDetectLog()

# get appkey information
appKeyFilename = APPKEY_FILENAME
appKeyfile = open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()

# get logdate from prompt
parser = argparse.ArgumentParser()
parser.add_argument('logdate', help='date with format YYYYMMDD')
parser.add_argument('-d','--dev', action='store_true', help='use dev server')
args = parser.parse_args()

# Server setup
servertype = 's3'
if args.dev:
    servertype = 'dev'

if isLogDown == True:
    downLogWorker = downlog.LogDownloader()
    downLogWorker.setLogInfo(args.logdate,logtype,servertype)
    downLogWorker.downLogRecord()

genDataFrameWorker = genDataFrame.DailyLogWorker()
genDataFrameWorker.init(logtype,args.logdate,appKey)

genDataFrameWorker.makeDailyLogfileList()
if len(genDataFrameWorker.mFileNameList) > 0:

    totalDataFrame      = DataFrame()
    currLogDataFrame    = DataFrame()
    print '# [runImportDetectLog] Number of logfile@ %s = %s' %(args.logdate,len(genDataFrameWorker.mFileNameList))
    print '# [runImportDetectLog] ------------------------------------------------------'

    while genDataFrameWorker.nextDailyLogFile():

        # data loading from a single file
        genDataFrameWorker.loadDailyLog('json')
        #data frame generation
        currLogDataFrame = genDataFrameWorker.getDailyDataFrame(-1)

        if not (currLogDataFrame.empty):
            currLogDataFrame.sort_values(by='deviceTime')

            # InvalidBeaconLogFrame = currLogDataFrame [ currLogDataFrame['isValidBeaconID'] == False]
            # ValidBeaconLogFrame   = currLogDataFrame [ currLogDataFrame['isValidBeaconID'] == True ]
            totalDataFrame = pd.concat([totalDataFrame, currLogDataFrame],ignore_index=True)
        # print '# [runImportDetectLog] currLogDataFrame of %s is %s' % (genDataFrameWorker.mFileNameList[genDataFrameWorker.mLogFileIndex - 1],currLogDataFrame.index.size)
        # print '# [runImportDetectLog] totalDataFrame of %s is %s' % (genDataFrameWorker.mFileNameList[genDataFrameWorker.mLogFileIndex - 1],totalDataFrame.index.size)
        print '# [runImportDetectLog] ------------------------------------------------------'




if isCSVwrite:
    if not (totalDataFrame.empty):

        if appKey == '5e228d8d-c869-437c-ae70-8dd87b089f64':
            appname = 'cash'
            print '# [runImportDetectLog] The current App is set to %s' % appKey
            print '# [runImportDetectLog] The current Appname is set to %s' % appname

        elif appKey == '6227368d-7a59-4805-a110-24b23e8c87b3':
            appname = 'clip'
            print '# [runImportDetectLog] The current App is set to %s' % appKey
            print '# [runImportDetectLog] The current Appname is set to %s' % appname
        else:
            appname = 'clip'
            print '# [runImportDetectLog] The default App is set to %s' % appKey
            print '# [runImportDetectLog] The current Appname is set to %s' % appname

        subprocess.check_call('mkdir '+cm.DAILY_DATAFRAME_DETECT_CSV_DIR,shell=True)
        subprocess.check_call('mkdir '+cm.DAILY_DATAFRAME_DETECT_CSV_DIR + '/' + appname,shell=True)

        LOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_DETECT_CSV_DIR + \
                                                     '/' + appname +\
                                                     '/' + args.logdate + '_' \
                                                         + logtype + 'Log_' + appname + '_'\
                                                         + 'DailyDataFrame' +'.csv'
        totalDataFrame.to_csv(LOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
        print '# [runImportDetectLog] CSV write done! @ %s' % LOG_DATAFRAME_CSV_FILENAME



