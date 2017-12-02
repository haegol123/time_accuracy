#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: runImportLog.py
# written by Soonwon Ka and Jaewook Kang @ Aug 2017
#------------------------------------------------------------
import sys
from os import getcwd
sys.path.insert(0,getcwd()+'/python_codes')

import downlog
import genDataFrame
import common as cm
from datetime import datetime
import datetime

import intro
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

import argparse
import subprocess
import time
from appkeylist import APPKEY_FILENAME, AppkeyList


isCSVwrite  = True
isLogDown   = True
isEXELog    = True


#  --- Log config ---

# if FrameSize == -1, take all items from the log
frameSize = -1

# intro
intro.intro_ImportLog()

# get arguments from prompt
parser = argparse.ArgumentParser()
# parser.add_argument('logdate', help='date with format YYYYMMDD, type number 10: if the logtype is schedule') #'schedule' logdate 필요없음 (개발 1단계)
# parser.add_argument('-an','--appname', default='clip', help='set the appname') # default 'clip'

parser.add_argument('logdate', help='date with format YYYYMMDD') #'schedule' logdate 필요없음
parser.add_argument('-an','--appname', default='clip', help='set the appname') # default 'clip'
parser.add_argument('-s','--server',  help= ' servername: s3, dev, v1(schedule file of s3),dev-schedule')
parser.add_argument('-t','--type', default='detect', help='set the log type') # default 'detect'
args = parser.parse_args()

'''
# Server setup
servertype = 's3' # 명령행에 입력 없을 시 default 's3' 상용
if args.dev:
    servertype = 'dev' # 개발 서버
'''
# schedule server(s3, dev, v1) 설정을 위하여 이렇게 설정
servertype=args.server
logtype = args.type

# get appkey information
aklist = AppkeyList()
aklist.setAppkeyList(args.appname)
appname = args.appname
appKey = aklist.getAppkey()


if isEXELog:
    exeLogfilename = cm.LOGFILE_DIR + '_' + appname +'.log'
    fp = open(exeLogfilename,'w')


if isEXELog:
    fp.write('# ================================================================\n')
    fp.write('# [AppkeyList]  - appname is set to \"%s\"\n' % aklist.appname)
    fp.write('# [AppkeyList]  - appkey is set to \"%s\"\n' % aklist.appkey)
    fp.write('# [AppkeyList] ----- init finished! ---------------------\n')


# # 1단계 때 사용한 것, 날짜를 default-> 로 받거나 고정값으로 받았을 경우
# if args.logdate == '10':
#     now = datetime.datetime.now()  # 현재 날짜를 불러옴
#     tmp = now.strftime('%Y%m%d')  # YYYYMMDD 형식 맞춰서 str포맷으로 반환
#     args.logdate = tmp

# Download logs
if isLogDown == True:
    downLogWorker = downlog.LogDownloader()
    if isEXELog:
        downLogWorker.setfile(fp)
    downLogWorker.setLogInfo(args.logdate,logtype,servertype,appKey)

    downLogWorker.downLogRecord()
    if isEXELog:
        downLogWorker.closefile()

#time.sleep(60 * 20)  # waiting for log download

# Conversion of log file into data frames
genDataFrameWorker = genDataFrame.DailyLogWorker()
genDataFrameWorker.setfile(fp)

genDataFrameWorker.init(logtype,args.logdate,appKey)
genDataFrameWorker.makeDailyLogfileList()

if len(genDataFrameWorker.mFileNameList) > 0:

    totalDataFrame      = DataFrame()
    currLogDataFrame    = DataFrame()
    print '# [runImportLog] Number of logfile@ %s = %s' %(args.logdate,len(genDataFrameWorker.mFileNameList))
    print '# [runImportLog] ------------------------------------------------------'

    if isEXELog:
        fp.write('# [runImportLog] Number of logfile@ %s = %s\n' %(args.logdate,len(genDataFrameWorker.mFileNameList)))
        fp.write('# [runImportLog] ------------------------------------------------------\n')


    while genDataFrameWorker.nextDailyLogFile():

        # data loading from a single file
        genDataFrameWorker.loadDailyLog('json')
        # data frame generation
        currLogDataFrame = genDataFrameWorker.getDailyDataFrame(-1)

        if not (currLogDataFrame.empty) and logtype != 'schedule' and logtype != 'monitoring':
            currLogDataFrame.sort_values(by='deviceTime')

            # InvalidBeaconLogFrame = currLogDataFrame [ currLogDataFrame['isValidBeaconID'] == False]
            # ValidBeaconLogFrame   = currLogDataFrame [ currLogDataFrame['isValidBeaconID'] == True ]
            totalDataFrame = pd.concat([totalDataFrame, currLogDataFrame],ignore_index=True)
        # print '# [runImportLog] currLogDataFrame of %s is %s' % (genDataFrameWorker.mFileNameList[genDataFrameWorker.mLogFileIndex - 1],currLogDataFrame.index.size)
        # print '# [runImportLog] totalDataFrame of %s is %s' % (genDataFrameWorker.mFileNameList[genDataFrameWorker.mLogFileIndex - 1],totalDataFrame.index.size)
        #schedule log
        totalDataFrame = pd.concat([totalDataFrame, currLogDataFrame], ignore_index=True)
else:

    print '# [runImportLog] There is no logfile to proceed!'
    isCSVwrite = False

    if isEXELog:
        fp.write('# [runImportLog] There is no logfile to proceed!\n')

genDataFrameWorker.closefile()


print '# [runImportLog] ------------------------------------------------------'

if isEXELog:
    fp.write('# [runImportLog] ------------------------------------------------------\n')

#csvfiles/dailyDataFrame/schedule
if isCSVwrite:
    if not (totalDataFrame.empty):

        print '# [runImportLog] The current App is set to %s' % appKey
        print '# [runImportLog] The current Appname is set to %s' % appname

        if isEXELog:
            fp.write('# [runImportLog] The current App is set to %s\n' % appKey)
            fp.write('# [runImportLog] The current Appname is set to %s\n' % appname)

        location = cm.Common().getDailyDataFrameCsvDir(logtype)

        try:
            subprocess.check_call('mkdir '+ location,shell=True)
        except:
            print '# [runImportLog] location = %s already exists' % location
            fp.write('# [runImportLog] location = %s already exists\n' % location)

        try:
            subprocess.check_call('mkdir ' + location + '/' + appname, shell=True)
        except:
            print '# [runImportLog] location/appname = %s already exists' % (location + '/' + appname)
            fp.write('# [runImportLog] location/appname = %s already exists\n' % (location + '/' + appname))


        LOG_DATAFRAME_CSV_FILENAME =     location + \
                                    '/' + appname +\
                                    '/' + args.logdate + '_' \
                                        + logtype + 'Log_' + appname + '_'\
                                        + 'DailyDataFrame' +'.csv'

        totalDataFrame.to_csv(LOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
        print '# [runImportLog] CSV write done! @ %s' % LOG_DATAFRAME_CSV_FILENAME
        if isEXELog:
            fp.write('# [runImportLog] CSV write done! @ %s\n' % LOG_DATAFRAME_CSV_FILENAME)
    else:
        print '# [runImportLog] The log is empty with respect to Appkey %s' % appKey
        if isEXELog:
            fp.write('# [runImportLog] The log is empty with respect to Appkey %s' % appKey)

if isEXELog:
    fp.close()
