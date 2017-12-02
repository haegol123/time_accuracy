#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: DataFrameForLog.py
# This script include classes to generation log data frame
#
# This is for Core performance measuring from CoreLogs
# written by Soonwon Ka @ Aug 2017
# final update at July 2017 by jwkang
#------------------------------------------------------------
import json
import sys
from os import getcwd, path
sys.path.insert(0, getcwd()+'/python_codes')

from datetime import datetime
from subprocess import check_output, CalledProcessError

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import common as cm
import validBeaconList
from appkeylist import REG_CLiP_APPKEY_LIST, REG_CASH_APPKEY_LIST

class DataFrameForLog(object):

    def __init__(self, dataFrame=DataFrame()):
        self.mDataFrame = dataFrame
        self.mFrameSize = 0

    def releaseFrame(self):
        del self.mDataFrame

    def resetFrame(self, dataFrame=DataFrame()):
        self.releaseFrame()
        self.mDataFrame = dataFrame
        self.mFrameSize = 0


    def importRecords(self,records,appkey,validBeaconSet):
        self.mDataFrame           = DataFrame(data=records)
        self.mFrameSize = self.mDataFrame.index.size

    def getDataFrame(self):
        return self.mDataFrame

    def getDataFrameSize(self):
        return self.mFrameSize

#---------------------------------------------------------------------------------------------------------
# class DataFrameForScheduleLog(DataFrameForLog):
#
#     def __init__(self):
#         DataFrameForLog.__init__(self)
#         self.mScheduleLogFrame = DataFrame(columns=cm.SCHEDULELOG_LABEL)
#
#     def resetFrame(self):
#         DataFrameForLog.resetFrame(self)
#         self.mScheduleLogFrame = DataFrame(columns=cm.SCHEDULELOG_LABEL)
#
#     def importRecords(self, records, appkey, validBeaconSet):
#
#         entireRecordFrame = DataFrame(data=records)
#         tmplist=[]
#         resultFrame=DataFrame()
#         tmp=None
#         tmpTimeList=[]
#         tmpSplittedList=[]
#         tmpStart=[]
#         tmpEnd=[]
#         tmpStartFrame = DataFrame()
#         tmpEndFrame = DataFrame()
#         tmpStartEndFrame= DataFrame()
#         tmpTimeFrame=DataFrame(columns=['beacon','start','end'])
#         tmpBeacon=None
#
#         if not (entireRecordFrame.empty):
#
#             # CustomLog processing
#             scheduleLogFrame = DataFrame(data=entireRecordFrame[cm.SCHEDULELOG_LABEL], columns=cm.SCHEDULELOG_LABEL)
#             tmplist=scheduleLogFrame[cm.SCHEDULE_LOG_PARSE_NAME].values[0]       #'schedule'
#
#             #tmplist에 스케줄이 beacon 값에 따라 나누어 담겨 있음 -> beacon 값에 따라 정리
#             for i in range(len(tmplist)):
#                 tmpSeries=Series(data=tmplist[i])
#                 tmpFrame=DataFrame(data=tmpSeries)
#                 tmpFrame=tmpFrame.T     #column index 위치 바꿈
#                 tmpBeacon=int(tmpFrame['beacon'])
#
#                 tmpTimeList = tmpFrame['time'].values[0]            #[] 형태 걸러내야됨
#
#                 #Time split(start/end) tmpTimeList 에 시간들이 담겨 있음
#                 for j in range(len(tmpTimeList)):
#
#                     tmpSplittedList = str(tmpTimeList[j]).split('/')
#                     tmpStart.append(str(tmpSplittedList[0]))
#                     tmpEnd.append(str(tmpSplittedList[1]))
#
#                 # 분할한 시간들을 Series 에 저장 dict 형태
#                 tmpStartSeries=Series(tmpStart)
#                 tmpEndSeries=Series(tmpEnd)
#
#                 #Series 로 나눠놓은 시간들을 DataFrame 에 옮겨 담은 후에 두 컬럼을 합친다
#                 tmpStartFrame = DataFrame(data=tmpStartSeries, columns=['start'])
#                 tmpEndFrame = DataFrame(data=tmpEndSeries, columns=['end'])
#                 tmpStartEndFrame=pd.concat([tmpStartFrame,tmpEndFrame], axis=1)     #concat으로 붙임
#
#                 # 그런데 시간만 합쳐진 프레임이므로 비콘값도 넣어두어야함
#
#                 tmpPartialFrame=DataFrame(columns=['beacon','start','end'])
#                 tmpPartialFrame=pd.concat([tmpPartialFrame,tmpStartEndFrame])
#                 tmpPartialFrame['beacon']=tmpBeacon
#
#                 #반복문 끝나기 전에 비콘 값에 따라 정리한 데이터 한곳에 모으면 끝
#                 resultFrame = pd.concat([resultFrame, tmpPartialFrame])
#
#             #resultFrame column order 재정렬
#             resultFrame=resultFrame[['beacon','start','end']]
#             self.mDataFrame = resultFrame
#             self.mFrameSize = self.mDataFrame.index.size
#             return True
#
#         else:
#             print '# [DataFrameForScheduleLog] The Schedule Log does not contain the appkey = %s' % appkey
#             self.mFrameSize = 0
#             return False
# ------------------------------------------------------------------------------------------------

class DataFrameForMonitoringLog(DataFrameForLog):

    def __init__(self):
        DataFrameForLog.__init__(self)
        self.mMonitoringLogFrame = DataFrame(columns=cm.MONITORINGLOG_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self)
        self.mMonitoringLogFrame = DataFrame(columns=cm.MONITORINGLOG_LABEL)

    def importRecords(self, records, appkey, validBeaconSet):
        entireRecordFrame = DataFrame(data=records)
        resultFrame = DataFrame()

        if not (entireRecordFrame.empty):
            monitoringLogFrame = DataFrame(data=entireRecordFrame[cm.MONITORINGLOG_LABEL], columns=cm.MONITORINGLOG_LABEL)

            resultFrame=monitoringLogFrame
            self.mDataFrame = resultFrame
            self.mFrameSize = self.mDataFrame.index.size
            return True

        else:
            print '# [DataFrameForScheduleLog] The Schedule Log does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

class DataFrameForScheduleLog(DataFrameForLog):

    def __init__(self):
        DataFrameForLog.__init__(self)
        self.mScheduleLogFrame = DataFrame(columns=cm.SCHEDULELOG_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self)
        self.mScheduleLogFrame = DataFrame(columns=cm.SCHEDULELOG_LABEL)

    def importRecords(self, records, appkey, validBeaconSet):

        entireRecordFrame = DataFrame(data=records)
        tmplist=[]
        resultFrame=DataFrame()
        tmp=None
        tmpTimeList=[]
        tmpSplittedList=[]

        tmpDetailsList=[]
        tmpStartFrame = DataFrame()
        tmpEndFrame = DataFrame()
        tmpStartEndFrame= DataFrame()
        tmpTimeFrame=DataFrame(columns=['beacon','broadcastchannel','start','end'])
        tmpBeacon=None

        if not (entireRecordFrame.empty):

            # CustomLog processing
            scheduleLogFrame = DataFrame(data=entireRecordFrame[cm.SCHEDULELOG_LABEL], columns=cm.SCHEDULELOG_LABEL)
            tmplist=scheduleLogFrame[cm.SCHEDULE_LOG_PARSE_NAME].values[0]       #'schedule'

            #tmplist에 스케줄이 beacon 값에 따라 나누어 담겨 있음 -> beacon 값에 따라 정리
            for i in range(len(tmplist)):
                tmpSeries=Series(data=tmplist[i])
                tmpBeacon=int(tmpSeries.get('beacon'))
                tmpDetailsList = tmpSeries.get('details')

                #beacon 안에서 details 의 구분에 따라 time 정리 필요
                for k in range(len(tmpDetailsList)):
                    tmpDetailsSeries=Series(data=tmpDetailsList[k])
                    tmpChannel=tmpDetailsSeries.get('broadcastchannel')
                    tmpTimeList = tmpDetailsSeries.get('time')           #[] 형태 걸러내야됨
                    tmpStart = []
                    tmpEnd = []

                    #Time split(start/end) tmpTimeList 에 시간들이 담겨 있음
                    for j in range(len(tmpTimeList)):
                        tmpSplittedList = str(tmpTimeList[j]).split('/')
                        tmpStart.append(str(tmpSplittedList[0]))
                        tmpEnd.append(str(tmpSplittedList[1]))

                # 분할한 time들을 각각 Series 에 저장 dict 형태
                    tmpStartSeries=Series(tmpStart)
                    tmpEndSeries=Series(tmpEnd)

                #Series 로 나눠놓은 시간들을 DataFrame 에 옮겨 담은 후에 두 컬럼을 합친다 이 떄 채널 정보도 일괄 추가
                    tmpStartFrame = DataFrame(data=tmpStartSeries, columns=['start'])
                    tmpEndFrame = DataFrame(data=tmpEndSeries, columns=['end'])
                    tmpStartEndFrame=pd.concat([tmpStartFrame,tmpEndFrame], axis=1)     #concat으로 붙임
                    tmpStartEndFrame['broadcastchannel']=tmpChannel

                # 그런데 채널,시간만 합쳐진 프레임이므로 비콘값도 넣어두어야함
                    tmpPartialFrame=DataFrame(columns=['beacon','broadcastchannel','start','end'])
                    tmpPartialFrame=pd.concat([tmpPartialFrame,tmpStartEndFrame])
                    tmpPartialFrame['beacon']=tmpBeacon

                #반복문 끝나기 전에 비콘,채널 값에 따라 정리한 time 데이터들을 한곳에 모으면 됨
                    resultFrame = pd.concat([resultFrame, tmpPartialFrame])

            #resultFrame column order 보기 좋게 재정렬
            resultFrame=resultFrame[['beacon','broadcastchannel','start','end']]
            self.mDataFrame = resultFrame
            self.mFrameSize = self.mDataFrame.index.size
            return True

        else:
            print '# [DataFrameForScheduleLog] The Schedule Log does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

class DataFrameForActiveLog(DataFrameForLog):
    def __init__(self):
        DataFrameForLog.__init__(self)
        # self.mActiveLogFrame = DataFrame(columns=cm.ACTIVELOG_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self)
        # self.mActiveLogFrame = DataFrame(columns=cm.ACTIVELOG_LABEL)

# ------------------------------------------------------------------------------------------------

class DataFrameForBeaconLog (DataFrameForLog):
    def __init__(self):
        DataFrameForLog.__init__(self, DataFrame(columns=cm.BEACONLOG_LABEL))
        self.mBeaconLogFrame = DataFrame(columns=cm.BEACONLOG_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self, DataFrame(columns=cm.BEACONLOG_LABEL))
        self.mBeaconLogFrame    = DataFrame(columns=cm.BEACONLOG_LABEL)


    def importRecords(self,records,appkey,validBeaconSet):

        entireRecordFrame           = DataFrame(data=records)
        self.mEntireRecordFrame = entireRecordFrame
        self.mBeaconLogFrame        = entireRecordFrame[cm.BEACONLOG_LABEL]

        try:
            self.mBeaconLogFrame    = self.mBeaconLogFrame  [ self.mBeaconLogFrame[cm.CORE_APPKEY_NAME] == appkey]
        except:
            pass

        if not(self.mBeaconLogFrame.empty):
            self.mDataFrame         = self.mBeaconLogFrame  [ self.mBeaconLogFrame[cm.BEACON_TRYCNT_NAME] > -1]
            self.mDataFrame         = self.mDataFrame       [ self.mDataFrame[cm.BEACON_SEQ_NAME] > -1]
            self.mDataFrame['deviceTime'] = [ datetime.fromtimestamp(long(elem*0.001)) for elem in self.mDataFrame['deviceTime'] ]

            self.mDataFrame         = self.mDataFrame.reset_index()
            beaconlogLen            = len(self.mDataFrame)

            isValidBeaconFrame     = DataFrame(columns=cm.BEACON_IS_VALID_BEACONNAME)

            # invalid beacon check
            for i in range(0,beaconlogLen):
                currBeaconID        = {str(self.mDataFrame[cm.BEACON_BEACON_NAME][i])}
                # print 'currBeaconID = %s' % currBeaconID
                # print 'validBeaconSet = %s' % validBeaconSet

                if currBeaconID.issubset(validBeaconSet):
                    isValidBeaconFrame.loc[i] = True
                else:
                    isValidBeaconFrame.loc[i] = False

                # print 'isValidBeaconFrame.loc[i] = %s' % isValidBeaconFrame.loc[i]

            self.mDataFrame         = pd.concat([ self.mDataFrame, isValidBeaconFrame],axis=1)
            self.mFrameSize = self.mDataFrame.index.size

            return True
        else:
            print '# [DataFrameForBeaconLog] The Beacon Log does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

#---------------------------------------------------------------------------------------------------------

class DataFrameForDetectLog (DataFrameForLog):
    def __init__(self):
        DataFrameForLog.__init__(self, DataFrame(columns=cm.DETECTLOG_LABEL))
        self.mLogFrame = DataFrame(columns=cm.DETECTLOG_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self, DataFrame(columns=cm.DETECTLOG_LABEL))
        self.mLogFrame          = DataFrame(columns=cm.DETECTLOG_LABEL)


    def importRecords(self,records,appkey,validBeaconSet):

        entireRecordFrame = DataFrame(data=records)

        #  appkey filtering
        try:
            entireRecordFrame = entireRecordFrame[ entireRecordFrame[cm.CORE_APPKEY_NAME] == appkey]
        except:
            entireRecordFrame = DataFrame()

        # content assistent filtering
        try:
            entireRecordFrame = entireRecordFrame[ entireRecordFrame[cm.DETECT_BEACON_NAME] > 0 ]
        except:
            entireRecordFrame = DataFrame()


        if not(entireRecordFrame.empty):

            # CustomLog processing
            customLogFrame                  = DataFrame(data=entireRecordFrame[cm.DETECTLOG_LABEL],columns=cm.DETECTLOG_LABEL)
            customLogFrame['deviceTime']    = [ datetime.fromtimestamp(long(elem*0.001)) for elem in customLogFrame['deviceTime'] ]

            # # core log type
            coreLogFrame         = entireRecordFrame[cm.CORE_NAME]
            isCoreNull           = np.logical_not(coreLogFrame.isnull())
            coreLogIndex         = coreLogFrame[isCoreNull].index


            ## parsing entireFrame['core']
            templist            = list(coreLogFrame.loc[coreLogIndex])
            isCoreDict          = Series(data=[str(type(elem)) == "<type 'dict'>" for elem in templist], \
                                     index=coreLogIndex)
            coreIndex           = isCoreDict[isCoreDict==True].index
            coreLogDataFrame    = DataFrame(data=list(coreLogFrame.loc[coreIndex]), \
                                        index=coreIndex)
            # coreLogDataFrame    = coreLogDataFrame.drop(cm.CORELOG_DATA_REMOVED_LABEL,axis=1)


            ### parsing coreLogDataFrame['data'] and merging the parsed columns into coreLogDataFrame
            if cm.DATA_NAME in coreLogDataFrame.columns: # If there exists a column named as cm.DATA_NAME
                coreLogSubJsonDataSequence           = coreLogDataFrame[cm.DATA_NAME]
                isCoreLogSubJsonDataSequenceNotNull  = np.logical_not(coreLogSubJsonDataSequence.isnull())
                coreLogSubJsonDataSequenceIndex      = coreLogSubJsonDataSequence[isCoreLogSubJsonDataSequenceNotNull].index

                coreLogSubJsonData    = list(coreLogSubJsonDataSequence.loc[coreLogSubJsonDataSequenceIndex])
                isCoreSubJsonDataDict = Series(data=[str(type(elem)) == "<type 'dict'>" for elem in coreLogSubJsonData], \
                                               index=coreLogSubJsonDataSequenceIndex)
                coreLogSubJsonDataIndex             = isCoreSubJsonDataDict[isCoreSubJsonDataDict==True].index
                coreLogSubJsonDataDataFrame = DataFrame(data=list(coreLogSubJsonDataSequence.loc[coreLogSubJsonDataIndex]),\
                                                        index=coreLogSubJsonDataIndex)
                coreLogDataFrame.drop(cm.DATA_NAME, axis=1, inplace=True)

                #    # Merge prev version w/o 'data' and new version w/ 'data'
                coreLogDataFrameTemp = coreLogDataFrame+coreLogSubJsonDataDataFrame
                coreLogDataFrameTemp[coreLogDataFrame.columns.values] = coreLogDataFrame

                col_list = list(coreLogSubJsonDataDataFrame.columns.values)
                idx_list = list(coreLogSubJsonDataSequenceIndex)
                coreLogDataFrameTemp.loc[idx_list, col_list] = coreLogSubJsonDataDataFrame.loc[idx_list, col_list]

                coreLogDataFrame = coreLogDataFrameTemp



            detectloglen  = len(entireRecordFrame)
            isValidBeaconFrame     = DataFrame(columns=cm.DETECT_IS_VALID_BEACONNAME)

            # invalid beacon check
            for i in range(0,detectloglen):
                currBeaconID        = {str(np.array(entireRecordFrame[cm.DETECT_BEACON_NAME],dtype=np.int64)[i])}
                # print 'currBeaconID = %s' % currBeaconID
                # print 'validBeaconSet = %s' % validBeaconSet

                if currBeaconID.issubset(validBeaconSet):
                    isValidBeaconFrame.loc[i] = True
                else:
                    isValidBeaconFrame.loc[i] = False
                # print 'isValidBeaconFrame.loc[i] = %s' % isValidBeaconFrame.loc[i]

            isValidBeaconFrame.index = entireRecordFrame.index
            # DataFrame concaternation
            self.mDataFrame = pd.concat([customLogFrame,coreLogDataFrame,isValidBeaconFrame],axis=1)
            self.mFrameSize = self.mDataFrame.index.size
            return True

        else:
            print '# [DataFrameForeDetectLog] The Detect Log does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

#------------------------------------------------------------------------------------------------#

class DataFrameForCustomLog (DataFrameForLog):
    def __init__(self):
        DataFrameForLog.__init__(self,DataFrame(columns=cm.CUSTOMLOG_CORE_LABEL))
        self.mLogFrame = DataFrame(columns=cm.CUSTOMLOG_CORE_LABEL)

    def resetFrame(self):
        DataFrameForLog.resetFrame(self, DataFrame(columns=cm.CUSTOMLOG_CORE_LABEL))
        self.mLogFrame          = DataFrame(columns=cm.CUSTOMLOG_CORE_LABEL)

    def importRecords(self,records,appkey,validBeaconSet):

        entireRecordFrame = DataFrame(data=records)

        #  appkey filtering
        # try:
        #     entireRecordFrame = entireRecordFrame[ entireRecordFrame[cm.CORE_APPKEY_NAME] == appkey]
        # except:
        #     entireRecordFrame = DataFrame()

        # content assistent filtering
        # try:
        #     entireRecordFrame = entireRecordFrame[ entireRecordFrame[cm.DETECT_BEACON_NAME] > 0 ]
        # except:
        #     entireRecordFrame = DataFrame()


        if not(entireRecordFrame.empty):

            # CustomLog processing
            customLogFrame                  = DataFrame(data=entireRecordFrame[cm.CUSTOMLOG_CORE_LABEL],columns=cm.CUSTOMLOG_CORE_LABEL)
            customLogFrame['deviceTime']    = [ datetime.fromtimestamp(long(elem*0.001)) for elem in customLogFrame['deviceTime'] ]

            ## parsing entireFrame['customLogs']
            coreLogFrame         = entireRecordFrame[cm.CORE_CUSTOM_LOG_PARSE_NAME]
            isCoreNull           = np.logical_not(coreLogFrame.isnull())
            coreLogIndex         = coreLogFrame[isCoreNull].index
            templist            = list(coreLogFrame.loc[coreLogIndex])
            isCoreDict          = Series(data=[str(type(elem)) == "<type 'dict'>" for elem in templist], \
                                     index=coreLogIndex)
            coreIndex           = isCoreDict[isCoreDict==True].index
            coreLogDataFrame    = DataFrame(data=list(coreLogFrame.loc[coreIndex]), \
                                        index=coreIndex)
            # coreLogDataFrame    = coreLogDataFrame.drop(cm.CORELOG_DATA_REMOVED_LABEL,axis=1)

            # ## parsing coreLogDataFrame['coreData']
            # coreDataUnparsedFrame         = coreLogDataFrame[cm.CORE_DATA_PARSE_NAME]
            # isCoreNull           = np.logical_not(coreDataUnparsedFrame.isnull())
            # coreLogIndex         = coreLogFrame[isCoreNull].index
            # templist            = list(coreDataUnparsedFrame.loc[coreLogIndex])
            # isCoreDict          = Series(data=[str(type(elem)) == "<type 'dict'>" for elem in templist], \
            #                          index=coreLogIndex)
            # coreIndex           = isCoreDict[isCoreDict==True].index
            # coreDataFrame    = DataFrame(data=list(coreDataUnparsedFrame.loc[coreIndex]), \
            #                             index=coreIndex)


            # detectloglen  = len(entireRecordFrame)
            # isValidBeaconFrame     = DataFrame(columns=cm.DETECT_IS_VALID_BEACONNAME)
            #
            # # invalid beacon check
            # for i in range(0,detectloglen):
            #     currBeaconID        = {str(np.array(entireRecordFrame[cm.DETECT_BEACON_NAME],dtype=np.int64)[i])}
            #     # print 'currBeaconID = %s' % currBeaconID
            #     # print 'validBeaconSet = %s' % validBeaconSet
            #
            #     if currBeaconID.issubset(validBeaconSet):
            #         isValidBeaconFrame.loc[i] = True
            #     else:
            #         isValidBeaconFrame.loc[i] = False
            #     # print 'isValidBeaconFrame.loc[i] = %s' % isValidBeaconFrame.loc[i]
            #
            # isValidBeaconFrame.index = entireRecordFrame.index

            # DataFrame concaternation
            # self.mDataFrame = pd.concat([customLogFrame, coreLogDataFrame, isValidBeaconFrame],axis=1)
            self.mDataFrame = pd.concat([customLogFrame, coreLogDataFrame],axis=1)
            self.mFrameSize = self.mDataFrame.index.size
            return True

        else:
            print '# [DataFrameForCustomLog] The Custom Log does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

#------------------------------------------------------------------------------------------------#



class DataFrameForCoreLog (DataFrameForLog):

    def __init__(self):
        DataFrameForLog.__init__(self)

    def importRecords(self,records,appkey,validBeaconSet):

        JsonRecords = [json.loads(eval) for eval in records]

        entireRecordFrame = DataFrame(data=JsonRecords)

        try:
            entireRecordFrame = entireRecordFrame[ entireRecordFrame[cm.CORE_APPKEY_NAME] == appkey]
        except:
            entireRecordFrame = DataFrame()

        if not(entireRecordFrame.empty):
            coreLogValues                   = entireRecordFrame[cm.CORELOG_NAME].values

            # CustomLog processing
            coreLogSize                     = [len(list1d) for list1d in coreLogValues]
            customLogFrame                  = DataFrame(data=entireRecordFrame[cm.CUMSTOMLOG_LABEL],columns=cm.CUMSTOMLOG_LABEL)
            customLogFrame['deviceTime']    = [ datetime.fromtimestamp(long(elem*0.001)) for elem in customLogFrame['deviceTime'] ]
            customLogIndex                  = np.cumsum(coreLogSize)
            customLogIndex                  = np.insert(customLogIndex,0,0) #insert 0 at first elem
            customLogIndex                  = np.delete(customLogIndex,-1)  # delete the last elem
            customLogFrame.index            = customLogIndex
            customLogFrame                  = customLogFrame.reindex(range(sum(coreLogSize)),method='ffill') # phone model interpolation


            coreLogFrame = DataFrame(data=[ elem for list1d in coreLogValues for elem in list1d])

            # # ed log type
            edLogFrame      = DataFrame(data=list(coreLogFrame[cm.ED_NAME].values))
            isEDPassFrame   = edLogFrame[cm.ED_ISENERGY_NAME]
            isDataNull      = np.logical_not(coreLogFrame[cm.CORE_DATA_NAME].isnull())
            edTrueIndex     = edLogFrame[np.logical_and(isEDPassFrame,isDataNull) ].index

            ## parsing coreLogs['data']
            templist            = list(coreLogFrame[cm.CORE_DATA_NAME].loc[edTrueIndex])
            isDataDict      = Series(data=[str(type(elem)) == "<type 'dict'>" for elem in templist], \
                                     index=edTrueIndex)
            dataIndex       = isDataDict[isDataDict==True].index
            dataLogFrame    = DataFrame(data=list(coreLogFrame[cm.CORE_DATA_NAME].loc[dataIndex]), \
                                        index=dataIndex)
            dataLogFrame    = dataLogFrame.drop(cm.CORELOG_DATA_REMOVED_LABEL,axis=1)


            dataLogFrame['isDataCsPass']        = [bool(elem) for elem in dataLogFrame['isDataCsPass']]
            dataLogFrame['isPreambleCsPass']    = [bool(elem) for elem in dataLogFrame['isPreambleCsPass']]
            isCRCpassFrame                      = DataFrame(    data= [bool(elem > -1) for elem in dataLogFrame['decodingResult']],\
                                                                 index=dataIndex,\
                                                                 columns=['isCRCPass'])
            CRCpassIndex                        = isCRCpassFrame[isCRCpassFrame['isCRCPass'] == True].index
            beaconIdFrame                       = DataFrame(   data=dataLogFrame['decodingResult'].loc[CRCpassIndex].values,\
                                                               index= CRCpassIndex,\
                                                               columns=['beaconID'])
            isVaildIDFrame                      = DataFrame(data=[ set(str(elem)).issubset(validBeaconSet) for elem in beaconIdFrame.values.flatten()],\
                                                            index=CRCpassIndex,\
                                                            columns=['isValidBeaconID'])
            # DataFrame concaternation
            self.mDataFrame = pd.concat([customLogFrame,edLogFrame,dataLogFrame,isCRCpassFrame,beaconIdFrame,isVaildIDFrame],axis=1)
            self.mFrameSize = self.mDataFrame.index.size
            return True
        else:
            print '# [DataFrameForeCoreLog] The coreLog does not contain the appkey = %s' % appkey
            self.mFrameSize = 0
            return False

    ####---------------------Legacy -----------------------------------
    # def importRecordsbyAppend(self,records,appkey,phoneModel,validBeaconSet):
    #     JsonRecords = [json.loads(eval) for eval in records]
    #
    #     for i in range(0, self.mFrameSize):
    #         # print '# [DataFrameForCoreLog] i = %s' % i
    #         # try:
    #         if JsonRecords[i]['appKey'] == appkey:
    #             self.appendToFrame(JsonRecords[i],validBeaconSet)
    #         # except:
    #         #     print ' #[DataFrameForCoreLog] CoreLog with index %s does not include "appKey: or "appName"' % i
    #         #     pass
    #

    # def appendToFrame(self,singleRecord,validBeaconSet):
    #
    #     entireRecordFrame = DataFrame(singleRecord)
    #     customLogFrame = entireRecordFrame[cm.CUMSTOMLOG_LABEL]
    #     coreLogFrame = entireRecordFrame[cm.CORELOG_NAME]
    #     coreLogSize = len(coreLogFrame)
    #     coreLogHeadFrame = DataFrame(columns=cm.CORELOG_HEAD_LABEL_FRAME)
    #     coreLogEDFrame   = DataFrame(columns=cm.CORELOG_ED_LABEL_FRAME)
    #     coreLogDataFrame = DataFrame(columns=cm.CORELOG_DATA_LABEL_FRAME)
    #
    #
    #     for i in range(0, coreLogSize):
    #         templist = []
    #         for j in range(0, len(cm.CORELOG_HEAD_LABEL)):
    #             templist.append(coreLogFrame[i][cm.CORELOG_HEAD_LABEL[j]])
    #         coreLogHeadFrame.loc[i] = templist
    #
    #         templist = []
    #         for j in range(0, len(cm.CORELOG_ED_LABEL)):
    #             templist.append(coreLogFrame[i]['ed'][cm.CORELOG_ED_LABEL[j]])
    #
    #         coreLogEDFrame.loc[i]   = templist
    #
    #         if coreLogFrame[i]['ed']['isEnergy'] == True:
    #             templist = []
    #             for j in range(0,len(cm.CORELOG_DATA_LABEL)):
    #                 if (cm.CORELOG_DATA_LABEL[j] is 'isDataCsPass') or (cm.CORELOG_DATA_LABEL[j] is 'isPreambleCsPass'):
    #                     templist.append(bool(coreLogFrame[i]['data'][cm.CORELOG_DATA_LABEL[j]]))
    #                 else:
    #                     templist.append(coreLogFrame[i]['data'][cm.CORELOG_DATA_LABEL[j]])
    #
    #             decodingResult = coreLogFrame[i]['data']['decodingResult']
    #             if  decodingResult > -1:
    #                 templist.append(True) # 'isCRCPasss'
    #                 templist.append(decodingResult) # 'signalID'
    #             else:
    #                 templist.append(False)
    #                 templist.append(-1)
    #
    #             if set(str(decodingResult)).issubset(validBeaconSet):
    #                 templist.append(True)  # isValidBeaconID
    #             else:
    #                 templist.append(False)  # isValidBeaconID
    #
    #             coreLogDataFrame.loc[i] = templist
    #
    #     self.mDataFrame = self.mDataFrame.append(pd.concat( [ customLogFrame, \
    #                                                           coreLogHeadFrame, \
    #                                                           coreLogEDFrame, \
    #                                                           coreLogDataFrame], \
    #                                                         axis=1),ignore_index =True)



