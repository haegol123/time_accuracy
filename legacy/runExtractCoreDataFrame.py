#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runExtractCoreDataFrame.py
# This is for extract  specific Log from entire dataframe

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------
import sys
from os import getcwd
from os import system
sys.path.insert(0,getcwd()+'/python_codes')

# import numpy as np
import intro

import pandas as pd
from pandas import DataFrame

isGetEDPASSLOG  = False
isGetPCSPASSLOG = True
isGetCRCPASSLOG = True

system('clear')

logdatelist = ['20170317',\
               '20170318',\
               '20170319',\
               '20170320',\
               '20170325']

intro.intro_extractCoreDataFrame()
print '# [runExtractDataFrame] Configuration'
print '# [runExtractDataFrame] isGetEDPASS = %s' % isGetEDPASSLOG
print '# [runExtractDataFrame] isGetPCSPASSLOG = %s' % isGetPCSPASSLOG
print '# [runExtractDataFrame] isGetCRCPASSLOG = %s' % isGetCRCPASSLOG
print '# -------------------------------------------------------------'
currDataFrame = DataFrame()
for i in range(0,len(logdatelist)):
    logdate = logdatelist[i]
    log_csvfilename = str(logdate) + '_coreLog_DailyDataFrame.csv'
    LOG_DATAFRAME_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_csvfilename

    currDataFrame = pd.read_csv(LOG_DATAFRAME_CSV_FILENAME)
    print '# [runExtractDataFrame] CSV reading done! @ %s' % LOG_DATAFRAME_CSV_FILENAME
    print '# [runExtractDataFrame] curr dataframe size is %s' % currDataFrame.index.size


    if isGetEDPASSLOG:
        # extract EDPASS log only
        currDataFrameEDPass = currDataFrame[currDataFrame['isEnergy'] == True]
        log_edpass_csvfilename = str(logdate) + '_coreLog_DailyDataFrameEDPASS.csv'
        LOG_DATAFRAME_EDPASS_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_edpass_csvfilename

        currDataFrameEDPass.to_csv(LOG_DATAFRAME_EDPASS_CSV_FILENAME,encoding='utf-8')
        print '# [runExtractDataFrame] CSV writing done! @ %s' % LOG_DATAFRAME_EDPASS_CSV_FILENAME
        print '# [runExtractDataFrame] extracted EDPASS curr dataframe size is %s' % currDataFrameEDPass.index.size

    if isGetPCSPASSLOG:
        # extract PCSPAss log only
        currDataFramePCSPASS = currDataFrame[currDataFrame['isPreambleCsPass'] == True]
        log_pcspass_csvfilename = str(logdate) + '_coreLog_DailyDataFramePCSPASS.csv'
        LOG_DATAFRAME_PCSPASS_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_pcspass_csvfilename

        currDataFramePCSPASS.to_csv(LOG_DATAFRAME_PCSPASS_CSV_FILENAME,encoding='utf-8')
        print '# [runExtractDataFrame] CSV writing done! @ %s' % LOG_DATAFRAME_PCSPASS_CSV_FILENAME
        print '# [runExtractDataFrame] extracted PCSPASS curr dataframe size is %s' % currDataFramePCSPASS.index.size



    if isGetCRCPASSLOG:
        # extract CRCPASS log only
        currDataFrameCRCPass = currDataFrame[currDataFrame['isCRCPass'] == True]

        log_crcpass_csvfilename = str(logdate) + '_coreLog_DailyDataFrameCRCPASS.csv'
        LOG_DATAFRAME_CRCPASS_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_crcpass_csvfilename

        currDataFrameCRCPass.to_csv(LOG_DATAFRAME_CRCPASS_CSV_FILENAME,encoding='utf-8')
        print '# [runExtractDataFrame] CSV writing done! @ %s' % LOG_DATAFRAME_CRCPASS_CSV_FILENAME
        print '# [runExtractDataFrame] extracted CRCPASS curr dataframe size is %s' % currDataFrameCRCPass.index.size

