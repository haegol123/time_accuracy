#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runImportCoreLog.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import sys
import time
from os import getcwd
from os import system
sys.path.insert(0, getcwd()+'/python_codes')


import genDataFrame
# import logAnalyzer
# import argparse
import intro
from appkeylist import APPKEY_FILENAME

import common as cm
import pandas as pd
from pandas import DataFrame


system ('clear')

isLogImport         = False
isDataFrameMerge    = False
isCSVwrite          = True
isCRCPASS_CSVwrite  = False

isDataAnalysis = True

# get logdate from input argument in the format of YYYYMMDD
logdate='20170317'


# get appkey information
appKeyFilename = APPKEY_FILENAME
appKeyfile =  open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()
logtype = 'core'

# intro
intro.intro_ImportCoreLog()

if isLogImport:
    # instance generation
    dailycorelogworker = genDataFrame.DailyLogWorker()
    coreLogDataFrame = DataFrame()

    if isCRCPASS_CSVwrite:
        coreLogDataFrame_CRCPASS = DataFrame()

    # corelogworker init and makefilelist
    dailycorelogworker.init(logtype,logdate,appKey)
    dailycorelogworker.makeDailyLogfileList()

    t = time.time()
    while dailycorelogworker.nextDailyLogFile():
        # data loading
        dailycorelogworker.loadDailyLog('grep')
        currDataFrame = dailycorelogworker.getDailyDataFrame(-1)
        if not (currDataFrame.empty):

            if isCRCPASS_CSVwrite:
                    currDataFrame_CRCPASS = currDataFrame[currDataFrame['isCRCPass']==True]
                    currDataFrame_CRCPASS = currDataFrame_CRCPASS[currDataFrame_CRCPASS['isValidBeaconID'] == True]

            if isDataFrameMerge:        # merge dataframe
                coreLogDataFrame = pd.concat([ coreLogDataFrame, currDataFrame],ignore_index=True)
                coreLogDataFrame_CRCPASS = pd.concat([ coreLogDataFrame_CRCPASS, currDataFrame_CRCPASS],ignore_index=True)
            else:
                coreLogDataFrame = currDataFrame
                coreLogDataFrame_CRCPASS = currDataFrame_CRCPASS

        # CSV file exporting
        if not(isDataFrameMerge):
            if isCSVwrite:
                if not (coreLogDataFrame.empty):
                    CORELOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
                                                     '/' + logdate + '_' \
                                                     + logtype + 'Log_' \
                                                     + 'DailyDataFrame'+ str(dailycorelogworker.mLogFileIndex) +'.csv'
                    coreLogDataFrame.to_csv(CORELOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
                    print '# [runDailyLogAnalysis] CSV write done! @ %s' % CORELOG_DATAFRAME_CSV_FILENAME

                if isCRCPASS_CSVwrite:
                    if not(coreLogDataFrame_CRCPASS.empty):
                        CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
                                                         '/' + logdate + '_' \
                                                         + logtype + 'Log_' \
                                                         + 'DailyDataFrameCRCPASS'+ str(dailycorelogworker.mLogFileIndex) +'.csv'
                        coreLogDataFrame_CRCPASS.to_csv(CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME, encoding='utf-8')
                        print '# [runDailyLogAnalysis] CSV write done! @ %s' % CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME


    # coreLogDataFrame_EDPASS = coreLogDataFrame[coreLogDataFrame['isEnergy'] == True]
    print '#----------------------------------------------------------------'

    if isDataFrameMerge:
        if isCSVwrite:
            if not (coreLogDataFrame.empty):
                CORELOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
                                                 '/' + logdate + '_' \
                                                 + logtype + 'Log_' \
                                                 + 'DailyDataFrame.csv'
                coreLogDataFrame.to_csv(CORELOG_DATAFRAME_CSV_FILENAME, encoding='utf-8')
                print '# [runDailyLogAnalysis] CSV write done! @ %s' % CORELOG_DATAFRAME_CSV_FILENAME

            if isCRCPASS_CSVwrite:
                if not (coreLogDataFrame_CRCPASS.empty):
                    CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
                                                             '/' + logdate + '_' \
                                                             + logtype + 'Log_' \
                                                             + 'DailyDataFrameCRCPASS.csv'
                    coreLogDataFrame_CRCPASS.to_csv(CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME, encoding='utf-8')
                    print '# [runDailyLogAnalysis] CSV write done! @ %s' % CORELOG_DATAFRAME_CRCPASS_CSV_FILENAME


    elapsed = time.time() - t
    print '# [runDailyLogAnalysis] Data loading and importing time = %s' % elapsed


# #--------------------------------dataFrame analysis--------------------------------------
# t = time.time()
# if isDataAnalysis:
#
#     if not(isLogImport):
#         CORELOG_DATAFRAME_CSV_FILENAME = cm.DAILY_DATAFRAME_CSV_DIR + \
#                                          '/' + logdate + '_' \
#                                          + logtype + 'Log_' \
#                                          + 'DailyDataFrame.csv'
#         coreLogDataFrame = DataFrame()
#         coreLogDataFrame = pd.read_csv(CORELOG_DATAFRAME_CSV_FILENAME)
#
#     dailyLogAnalyzer = logAnalyzer.DailyLogAnalysisWorker()
#     dailyLogAnalyzer.setDataFrame(coreLogDataFrame)
#
#     while dailyLogAnalyzer.nextPhoneModel():
#         dailyLogAnalyzer.updateCurrPhoneModelResult()
#
#     dailyLogAnalyzer.updateAvgMeasureResult()
#     dailyMeasureDataFrame       = dailyLogAnalyzer.getDailyMeasureDataFrame()
#     dailyFalseAlarmDataFrame    = dailyLogAnalyzer.getFalseAlarmEvent()
#     elapsed = time.time() - t
#     print  '# [runDailyLogAnalysis] Data analysis time = %s\n' % elapsed
#
#     # CSV file write
#     if isCSVwrite:
#         if not(dailyMeasureDataFrame.empty):
#             CORE_PERF_DATAFRAME_CSV_FILENAME = cm.DAILY_PERF_CSV_DIR  + \
#                                         '/' + logdate + '_' \
#                                             + logtype + 'PerfMeasure_' \
#                                             + 'DailyDataFrame.csv'
#             dailyMeasureDataFrame.to_csv(CORE_PERF_DATAFRAME_CSV_FILENAME,encoding='utf-8')
#
#         if not(dailyFalseAlarmDataFrame.empty):
#             CORE_FALSE_ALARM_CSV_FILENAME = cm.DAILY_FA_REPORT_CSV_DIR  + \
#                                         '/' + logdate + '_' \
#                                             + logtype + 'FalseAlarm_' \
#                                             + 'DailyDataFrame.csv'
#             dailyFalseAlarmDataFrame.to_csv(CORE_FALSE_ALARM_CSV_FILENAME,encoding='utf-8')
#
# else:
#     print '# [runDailyLogAnalysis] DataAnalysis is configured to \'OFF\''
#




