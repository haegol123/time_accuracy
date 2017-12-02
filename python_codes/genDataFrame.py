#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: genDateFrame.py
# This script include classes to generation log data frame
#
# This is for Core performance measuring from CoreLogs
# written by Jaewook Kang @ Mar 2017
# final update at July 2017 by jwkang
#------------------------------------------------------------
import json
import sys
from os import getcwd, path
sys.path.insert(0, getcwd()+'/python_codes')

from datetime import datetime
from subprocess import check_output, CalledProcessError
import gzip

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import common as cm
import validBeaconList
from appkeylist import REG_CLiP_APPKEY_LIST, REG_CASH_APPKEY_LIST, REG_USER_APPKEY_LIST
from DataFrameForLog import DataFrameForDetectLog, DataFrameForCustomLog, DataFrameForCoreLog,\
    DataFrameForActiveLog, DataFrameForBeaconLog, DataFrameForScheduleLog, DataFrameForMonitoringLog



class LogProfile (object):
    def __init__(self):
        self.mLogType = None
        self.mLogcurrdate = None
        self.mAppKey = None
        self.mLogDirPath = None

    def set(self,logtype,logdate,appkey):
        self.mLogType = logtype
        self.mLogcurrdate = logdate
        self.mAppKey      = appkey

        # common.getLogDirPath()로 method화 할 것
        if self.mLogType == 'core':
            self.mLogDirPath = cm.RAW_CORELOG_DIR
        elif self.mLogType == 'beacon':
            self.mLogDirPath = cm.RAW_BEACONLOG_DIR
        elif self.mLogType == 'schedule':
            self.mLogDirPath = cm.RAW_SCHEDULE_DIR
        elif self.mLogType == 'active':
            self.mLogDirPath = cm.RAW_ACTIVE_DIR
        elif self.mLogType == 'detect':
            self.mLogDirPath = cm.RAW_DETECT_DIR
        elif self.mLogType == 'custom':
            self.mLogDirPath = cm.RAW_CUSTOM_DIR
        elif self.mLogType == 'monitoring':
            self.mLogDirPath = cm.RAW_MONITORING_DIR
        else:
            self.mLogInfo.mLogDirPath = cm.RAW_CORELOG_DIR


class DailyLogWorker (object):

    def __init__(self):
        self.mLogInfo = LogProfile()
        self.mLogFileIndex = 0
        self.mLogFileName = None
        self.mFileNameList = []
        self.mRecords =[]
        self.mDataFrameForLog = None
        self.mValidBeaconSet = None
        self.mIsFileWrite = False
        self.mFp = None

    # def setPhoneModel(self,phoneModel):
    #     self.mLogInfo.mPhoneModel = phoneModel

    def setfile(self,fp):
        # self.mFp = open(filename,'w')
        self.mFp = fp
        self.mIsFileWrite = True
        print '[DailyLogWorker] mIsFileWrite = %s' % self.mIsFileWrite

    def closefile(self):
        # self.mFp.close()
        self.mIsFileWrite = False
        print '[DailyLogWorker] mIsFileWrite = %s' % self.mIsFileWrite



    def init(self,logtype,logdate,appkey):

        self.mLogInfo.set(logtype,logdate,appkey)

        # common.buildDataFrameForLog()로 method화 할 것
        if self.mLogInfo.mLogType == 'core':
            self.mDataFrameForLog = DataFrameForCoreLog()
        elif self.mLogInfo.mLogType == 'beacon':
            self.mDataFrameForLog = DataFrameForBeaconLog()
        elif self.mLogInfo.mLogType == 'schedule':
            self.mDataFrameForLog = DataFrameForScheduleLog()
        elif self.mLogInfo.mLogType == 'active':
            self.mDataFrameForLog = DataFrameForActiveLog()
        elif self.mLogInfo.mLogType == 'detect':
            self.mDataFrameForLog = DataFrameForDetectLog()
        elif self.mLogInfo.mLogType == 'custom':
            self.mDataFrameForLog = DataFrameForCustomLog()
        elif self.mLogInfo.mLogType == 'monitoring':
            self.mDataFrameForLog = DataFrameForMonitoringLog()
        else:
            self.mDataFrameForLog = DataFrameForCoreLog()

        #측정 데이터 가져오기
        userSet     = set(REG_USER_APPKEY_LIST)

        clipSet     = set(REG_CLiP_APPKEY_LIST)
        cashset     = set(REG_CASH_APPKEY_LIST)
        inputSet    = set([self.mLogInfo.mAppKey])

        isSubsetOfUser = inputSet.issubset(userSet)     #측정 데이터
        isSubsetOfCliP = inputSet.issubset(clipSet)
        isSubsetOfCashSlide = inputSet.issubset(cashset)

        print '# [DailyLogWorker] DailyLogWorker is initialized.'
        print '# [DailyLogWorker] - Logtype = %s' % self.mLogInfo.mLogType
        print '# ]DailyLogWorker] - LogDate = %s' % self.mLogInfo.mLogcurrdate
        print '# [DailyLogWorker] - CLiP AppKey Set = %s' % clipSet
        print '# [DailyLogWorker] - CLiP validBeaconSet = %s' % validBeaconList.CLiPBeaconSet
        print '# [DailyLogWorker] - CashSlide AppKey set = %s' % cashset
        print '# [DailyLogWorker] - CashSlide validBeaconSet = %s' % validBeaconList.CashSlideBeaconSet


        if self.mIsFileWrite:
            self.mFp.write('# [DailyLogWorker] DailyLogWorker is initialized.\n')
            self.mFp.write('# [DailyLogWorker] - Logtype = %s\n' % self.mLogInfo.mLogType)
            self.mFp.write('# ]DailyLogWorker] - LogDate = %s\n' % self.mLogInfo.mLogcurrdate)
            self.mFp.write('# [DailyLogWorker] - CLiP AppKey Set = %s\n' % clipSet)
            self.mFp.write('# [DailyLogWorker] - CLiP validBeaconSet = %s\n' % validBeaconList.CLiPBeaconSet)
            self.mFp.write('# [DailyLogWorker] - CashSlide AppKey set = %s\n' % cashset)
            self.mFp.write('# [DailyLogWorker] - CashSlide validBeaconSet = %s\n' % validBeaconList.CashSlideBeaconSet)


        if isSubsetOfCliP:
            self.mValidBeaconSet = validBeaconList.CLiPBeaconSet
            print '# [DailyLogWorker] - Current Appkey = %s' % self.mLogInfo.mAppKey
            if self.mIsFileWrite:
                self.mFp.write('# [DailyLogWorker] - Current Appkey = %s\n' % self.mLogInfo.mAppKey)

            returnvalue = True
        elif isSubsetOfCashSlide:
            self.mValidBeaconSet = validBeaconList.CashSlideBeaconSet
            print '# [DailyLogWorker] - Current Appkey = %s' % self.mLogInfo.mAppKey
            if self.mIsFileWrite:
                self.mFp.write('# [DailyLogWorker] - Current Appkey = %s\n' % self.mLogInfo.mAppKey)

            returnvalue = True
        #측정 데이터 값 가져오기
        elif isSubsetOfUser:
            self.mValidBeaconSet = validBeaconList.UserBeaconSet
            print '# [DailyLogWorker] - Current Appkey = %s' % self.mLogInfo.mAppKey
            if self.mIsFileWrite:
                self.mFp.write('# [DailyLogWorker] - Current Appkey = %s\n' % self.mLogInfo.mAppKey)

            returnvalue = True

        else:
            print '# [DailyLogWorker] The current Appkey is not supported.'
            if self.mIsFileWrite:
                self.mFp.write('# [DailyLogWorker] The current Appkey is not supported.\n')

            returnvalue = False
        print '#----------------------------------------------------------------'
        return returnvalue


    def setCurrfilename(self):
        self.mLogFileName = self.mLogInfo.mLogDirPath + '/' \
                      + self.mLogInfo.mLogcurrdate    + '/' \
                      + self.mFileNameList[self.mLogFileIndex]
        # print '# [DailyLogWorker] CurrFileName is set to %s' % self.mLogFileName


    def makeDailyLogfileList(self):
        try:
            if self.mLogInfo.mLogType == 'schedule':
                self.mFileNameList = check_output('ls ' + self.mLogInfo.mLogDirPath + '/' \
                                                  + self.mLogInfo.mLogcurrdate, shell=True)

            else:
            # 20170802 appkey로 필터링 추가 필
                self.mFileNameList = check_output('ls ' + self.mLogInfo.mLogDirPath + '/' \
                                                    + self.mLogInfo.mLogcurrdate \
                                                    + " | grep " + self.mLogInfo.mAppKey, shell = True)  # schedule file 은 한개지만.. 일단 리스트에 넣자
            #For schedule

            self.mFileNameList = self.mFileNameList.split()
            print '# [makeDailyLogfileList] FileNameList:',
            print self.mFileNameList

            if self.mIsFileWrite:
                self.mFp.write('# [makeDailyLogfileList] FileNameList:\n')
                self.mFp.write(str(self.mFileNameList) + '\n')

        except CalledProcessError:
            self.mFileNameList = []
            print '# [makeDailyLogfileList] LogFileList is empty.'
            if self.mIsFileWrite:
                self.mFp.write('# [makeDailyLogfileList] LogFileList is empty.\n')


    def nextDailyLogFile(self):

        if (self.mLogFileIndex < len(self.mFileNameList)) and (len(self.mFileNameList) > 0):
            self.setCurrfilename()
            self.mLogFileIndex += 1
            return True
        else:
            print '# [nextDailyLogFile] The LogfileList @ %s is empty.' % self.mLogInfo.mLogcurrdate
            if self.mIsFileWrite:
                self.mFp.write('# [nextDailyLogFile] The LogfileList @ %s is empty.\n' % self.mLogInfo.mLogcurrdate)
            return False


    def loadDailyLog(self,loadingType):
        if self.mLogFileIndex > 0:


            if (loadingType is 'grep') and (self.mLogInfo.mLogType is 'core'):
                print '# [DailyLogWorker] GREP Loading CoreLog file @ %s' % self.mFileNameList[self.mLogFileIndex - 1]
                if self.mIsFileWrite:
                    self.mFp.write('# [DailyLogWorker] GREP Loading CoreLog file @ %s\n' % self.mFileNameList[self.mLogFileIndex - 1])

                try:
                    # if self.mLogInfo.mPhoneModel == '*':
                    self.mRecords = check_output('cat ' + self.mLogFileName \
                                                        + '| grep ' + '\'"appKey":\"'   \
                                                        + self.mLogInfo.mAppKey + '\"\'', shell = True )
                    # else:
                    #     self.mRecords = check_output('cat ' + self.mLogFileName \
                    #                                                     + '| grep ' + '\'"appKey":\"'    \
                    #                                         + self.mLogInfo.mAppKey + '\"\'' \
                    #                                                     + '| grep ' + '\'"phoneModel":\"' \
                    #                                         + self.mLogInfo.mPhoneModel + '\"\'', shell = True)
                    self.mRecords.replace('\n',',\n')
                    self.mRecords = self.mRecords.split('\n')
                    self.mRecords.pop()
                except CalledProcessError:
                    self.mRecords = []
                    print '# [loadDailyLog] GREP does not work with the current appkey.'
                    if self.mIsFileWrite:
                        self.mFp.write('# [loadDailyLog] GREP does not work with the current appkey.\n')

            else:
                if loadingType is 'grep':
                    print '# [loadDailyLog] Loading type "grep" is supported only for Core log.'
                    print '# [loadDailyLog] Loading Log by JSON method'

                    if self.mIsFileWrite:
                        self.mFp.write('# [loadDailyLog] Loading type "grep" is supported only for Core log.\n')
                        self.mFp.write('# [loadDailyLog] Loading Log by JSON method.\n')

                print '# [loadDailyLog] JSON Loading CoreLog file @ %s' % self.mFileNameList[self.mLogFileIndex - 1]

                if self.mIsFileWrite:
                    self.mFp.write('# [loadDailyLog] JSON Loading CoreLog file @ %s\n' % self.mFileNameList[self.mLogFileIndex - 1])

                # schedule log
                if self.mLogInfo.mLogType == 'schedule' or self.mLogInfo.mLogType == 'custom':
                    mRecord = [json.loads(line) for line in open(self.mLogFileName)]  # depricated by using gzip since 9 2017
                else:
                    mRecord = [json.loads(line) for line in gzip.open(self.mLogFileName)]


                self.mRecords = mRecord
        else:
            print '# [loadDailyLog] The LogfileList @ %s is empty.' % self.mLogInfo.mLogcurrdate
            if self.mIsFileWrite:
                self.mFp.write('# [loadDailyLog] The LogfileList @ %s is empty.\n' % self.mLogInfo.mLogcurrdate)

        print '# [loadDailyLog] Log Loading Done!'
        if self.mIsFileWrite:
            self.mFp.write('# [loadDailyLog] Log Loading Done!\n')


    def getDailyDataFrame(self,frameSize):

        # reset self.mDataFrameForLog
        self.mDataFrameForLog.resetFrame()

        # set the frame size
        if frameSize == -1: # 전체 레코드
            self.mDataFrameForLog.mFrameSize = len(self.mRecords)
        else: # 일부 레코드
            self.mDataFrameForLog.mFrameSize = frameSize

        # import the data of self.mRecords to self.mDataFrameForLog's data frame
        print '# [getDailyDataFrame] Log Importing from %s' % self.mFileNameList[self.mLogFileIndex - 1]
        self.mDataFrameForLog.importRecords(self.mRecords,self.mLogInfo.mAppKey,self.mValidBeaconSet)
        # self.mDataFrameForLog.importRecordsbyAppend(self.mRecords,self.mLogInfo.mAppKey,self.mLogInfo.mPhoneModel,self.mValidBeaconSet)
        print '# [getDailyDataFrame] Log Importing Done!'
        print '# [getDailyDataFrame] DataFrameSize of %s is %s' % (self.mFileNameList[self.mLogFileIndex - 1],self.mDataFrameForLog.mFrameSize)
        print '#----------------------------------------------------------------'


        if self.mIsFileWrite:
            self.mFp.write('# [getDailyDataFrame] Log Importing from %s\n' % self.mFileNameList[self.mLogFileIndex - 1])
            self.mFp.write('# [getDailyDataFrame] Log Importing Done!\n')
            self.mFp.write('# [getDailyDataFrame] DataFrameSize of %s is %s\n' % (self.mFileNameList[self.mLogFileIndex - 1],self.mDataFrameForLog.mFrameSize))
            self.mFp.write('#----------------------------------------------------------------\n')
        # return the imported data frame result
        return self.mDataFrameForLog.getDataFrame()

    # # ------------------------------------------------------------------------------------------------
    # # JiSoo codes 2017 Apr
    # def get_file_name(self, index):
    #     mLogFileName = self.mLogInfo.mLogDirPath + '/' \
    #                   + self.mLogInfo.mLogcurrdate    + '/' \
    #                   + self.mFileNameList[index]
    #     return mLogFileName
    #
    # def load_daily_log(self,loadingType,file_list_index):
    #     if loadingType is 'grep':
    #         print '# [DailyLogWorker] GREP Loading CoreLog file @ %s' % self.mFileNameList[file_list_index]
    #         try:
    #             # if self.mLogInfo.mPhoneModel == '*':
    #             self.mRecords = check_output('cat ' + self.get_file_name(file_list_index) \
    #                                           + '| grep ' + '\'"appKey":\"'   \
    #                                           + self.mLogInfo.mAppKey + '\"\'', shell = True )
    #
    #             self.mRecords.replace('\n',',\n')
    #             self.mRecords = self.mRecords.split('\n')
    #             self.mRecords.pop()
    #         except CalledProcessError:
    #             self.mRecords = []
    #             print '# [DailyLogWorker] GREP does not work with the current appkey.'
    #
    #     elif loadingType is 'json':
    #         print '# [DailyLogWorker] JSON Loading CoreLog file @ %s' % self.mFileNameList[file_list_index]
    #         mRecord = [json.loads(line) for line in open(self.get_file_name(file_list_index))]  # 스케쥴 록 export
    #         self.mRecords += mRecord
    #     print '# [DailyLogWorker] Log Loading Done!'
    #
    # def get_daily_data_frame(self,frameSize):
    #     if frameSize == -1: # 전체 레코드
    #         self.mDataFrameForLog.mFrameSize = len(self.mRecords)
    #     else: # 일부 레코드
    #         self.mDataFrameForLog.mFrameSize = frameSize
    #     for mFile in self.mFileNameList:
    #         print '# [DailyLogWorker] Log Importing from %s' % mFile
    #         print '# [DailyLogWorker] Log Importing from %s' % mFile
    #     self.mDataFrameForLog.importRecords(self.mRecords,self.mLogInfo.mAppKey,self.mValidBeaconSet)
    #     # self.mDataFrameForLog.importRecordsbyAppend(self.mRecords,self.mLogInfo.mAppKey,self.mLogInfo.mPhoneModel,self.mValidBeaconSet)
    #     print '# [DailyLogWorker] Log Importing Done!'
    #     file_name = '{}_beaconLog_DailyDataFrame'.format(self.mLogInfo.mLogcurrdate)
    #
    #     print '# [DailyLogWorker] DataFrameSize of %s is %s' % ('',self.mDataFrameForLog.mDataFrame.index.size)
    #     print '#----------------------------------------------------------------'
    #
    #     return self.mDataFrameForLog.getDataFrame()
    #
    # def get_log_files(self,loadingType):
    #     mDirectoryList = []
    #     mFileNameList = []
    #     try:
    #         mDirectoryList = check_output('ls ' + self.mLogInfo.mLogDirPath + '/' \
    #                                                 + self.mLogInfo.mLogcurrdate, shell=True)
    #         mDirectoryList = mDirectoryList.split()
    #         if mDirectoryList[0][:22] == 'soundllyLog_beacon.log':
    #             self.mFileNameList = mDirectoryList
    #         else:
    #             for file in mDirectoryList:
    #                 mFiles = check_output('ls ' + self.mLogInfo.mLogDirPath + '/' \
    #                                             + self.mLogInfo.mLogcurrdate + '/' + file
    #                                       , shell=True)
    #                 mFiles = mFiles.split()
    #                 for idx, val in enumerate(mFiles):
    #                     mFiles[idx] = '{}/{}'.format(file, val)
    #                 mFileNameList += mFiles
    #             self.mFileNameList = mFileNameList
    #         print '# [DailyLogWorker] FileNameList:',
    #         print self.mFileNameList
    #
    #     except CalledProcessError:
    #         self.mFileNameList = []
    #         print '# [DailyLogWorker] LogFileList is empty.'
    #
    #     for idx, val in enumerate(self.mFileNameList):
    #         self.load_daily_log(loadingType, idx)
    #     # --- the end of Jisoo code -------------#

