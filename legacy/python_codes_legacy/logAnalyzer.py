#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: genDateFrame.py
# This script include classes for calculating core perfomance
#
# This is for Core performance measuring in the corecloud
# written by Jaewook Kang and Soonwon Ka @ Mar 2017
#------------------------------------------------------------

from __future__ import division
from pandas import Series,DataFrame
import pandas as pd
import python_codes.common as cm
#import validBeaconList

MEASURE_NAME = ['Log Rcvd Rate (%)','Log False-alarm Rate (%)', \
                'pCS true-pos. Rate (%)','pCS false-pos. Rate (%)',\
                'dCS true-pos. Rate (%)','dCS false-pos. Rate (%)',\
                'Avg. RicianKfactor (dB)','# of LOS ch.','# of NLOS ch.',\
                'Avg. SpreadingTime (sec)']


#-----------------------------------------------------------------------------#

class DailyLogAnalysisWorker(object):
    def __init__(self):
        self.mDailyDataFrame        = DataFrame()
        self.mCurrPhoneModelFrame   = DataFrame()
        self.mFalseAlarmDataFrame   = DataFrame()
        self.mMeasureDataFrame      = DataFrame(columns=MEASURE_NAME)
        self.mIsDailyDataFrame = False
        self.mCntStatAnalysis = CntStatAnalysis()
        self.mStatAnalysis = StatAnalysis()
        self.mRateStatAnalysis = RateStatAnalysis()
        self.mPhoneModel = 'default'
        self.mPhoneModelList = []
        self.mPhoneModelIndex = 0

    def reset(self):
        self.mDailyDataFrame        = DataFrame()
        self.mCurrPhoneModelFrame   = DataFrame()
        self.mFalseAlarmDataFrame   = DataFrame()
        self.mMeasureDataFrame          = DataFrame(columns=MEASURE_NAME)
        self.mIsDailyDataFrame = False
        self.mCntStatAnalysis.reset()
        self.mStatAnalysis.reset()
        self.mRateStatAnalysis.reset()
        self.mPhoneModel = 'default'
        self.mPhoneModelList = []
        self.mPhoneModelIndex = 0



    def setDataFrame(self, currCoreDataFrame):
        if self.mIsDailyDataFrame == False:
            self.mDailyDataFrame = currCoreDataFrame
            self.mPhoneModelList = list(set(self.mDailyDataFrame['phoneModel']))
            print '#----------------------------------------------------------------'
            print '# [DailyLogAnalysisWorker] mPhoneModelList = %s' % self.mPhoneModelList

            # list empty check
            if len(self.mPhoneModelList) < 1:
                print '# [DailyLogAnalysisWorker] phonelist is empty.'
                self.mIsDailyDataFrame = False
            else:
                self.mIsDailyDataFrame = True
        else:
            print '# [DailyLogAnalysisWorker] self.mDailyDataFrame has been already set!'

        return self.mIsDailyDataFrame


    def setCurrPhoneModel(self):

        if self.mPhoneModelIndex < len(self.mPhoneModelList):
            self.mPhoneModel = self.mPhoneModelList[self.mPhoneModelIndex]
            self.mCurrPhoneModelFrame =  self.mDailyDataFrame[self.mDailyDataFrame['phoneModel'] == self.mPhoneModel]
            return True
        else:
            return False


    def setPhoneModel(self,*phoneModel):

        entireSet = set(self.mPhoneModelList)
        inputSet = set(phoneModel)
        isSubset = inputSet.issubset(entireSet)
        print 'phoneModel   = %s' % phoneModel

        if self.mPhoneModelList and isSubset:
            self.mPhoneModel = phoneModel[0]
            self.mCurrPhoneModelFrame =  self.mDailyDataFrame[self.mDailyDataFrame['phoneModel'] == self.mPhoneModel]
            return True
        else:
            print '# [DailyLogAnalysisWorker] Improper phone Model!'
            return False

    def getPhoneModelAnalysis(self):
        self.mCntStatAnalysis.setStat(self.mCurrPhoneModelFrame)
        self.mStatAnalysis.setStat(self.mCurrPhoneModelFrame)
        self.mRateStatAnalysis.setStat(self.mCntStatAnalysis, self.mStatAnalysis)

    def nextPhoneModel(self):
        if( self.mPhoneModelIndex < len(self.mPhoneModelList)) and ( len(self.mPhoneModelList) > 0):
            self.setCurrPhoneModel()
            self.mPhoneModelIndex += 1
            print '# [DailyLogAnalysisWorker] The current PhoneModel is set to %s' % self.mPhoneModel
            return True
        else:
            print '# [DailyLogAnalysisWorker] The phone Model list is empty'
            return False


    def updateCurrPhoneModelResult(self):
        if self.mPhoneModelIndex > 0:
            self.getPhoneModelAnalysis()
            self.mMeasureDataFrame.loc[self.mPhoneModelList[self.mPhoneModelIndex - 1]] = self.mRateStatAnalysis.getMeasureList()
            self.display()
            return True
        else:
            print '# [DailyLogAnalysisWorker] The phone Model list is empty'
            return False


    def updateAvgMeasureResult(self):
        templist = []
        for i in range(0,len(MEASURE_NAME)):
            data =  self.mMeasureDataFrame[MEASURE_NAME[i]]
            if MEASURE_NAME[i] == 'Avg. RicianKfactor dB':
                data = data [ data != False]
            else:
                data = data [ data > -1.0]
            if len(data) > 0:
                templist.append(data.mean())
            else:
                templist.append(-1.0)
        self.mMeasureDataFrame.loc['Avg'] = templist
        print '#----------------------------------------------------------------'


    def getCurrPhoneModelDataFrame(self):
        print '# [DailyLogAnalysisWorker] Current PhoneModel is %s' % self.mPhoneModel
        return self.mCurrPhoneModelFrame

    def getFalseAlarmEvent(self):
        self.mFalseAlarmDataFrame = self.mDailyDataFrame[self.mDailyDataFrame['isValidBeaconID'] == False]
        if len(self.mFalseAlarmDataFrame)  < 1:
            print '# [DailyLogAnalysisWorker] No FalseAlarmEvents'
        return self.mFalseAlarmDataFrame



    def getDailyDataFrame(self,*phoneModel):

        entireSet = set(self.mPhoneModelList)
        inputSet = set(phoneModel)
        isSubset = inputSet.issubset(entireSet)
        print 'phoneModel   = %s' % phoneModel

        if not(phoneModel):
            return self.mDailyDataFrame
        elif phoneModel[0] == '*':
            return self.mDailyDataFrame
        elif self.mPhoneModelList and isSubset:
            return self.mDailyDataFrame[self.mDailyDataFrame['phoneModel'] == phoneModel[0]]
        else:
            print '# [DailyLogAnalysisWorker] The current PhoneModel is not found.'


    def getDailyMeasureDataFrame(self):
        return self.mMeasureDataFrame


    def display(self):
        # print '# [DailyLogAnalysisWorker]  PhoneModel = %s' % self.mPhoneModel
        self.mRateStatAnalysis.display()




# -----------------------------------------------------------------------------#


# class WeeklyLogAnalysisWorker(object):
#
#     def __init__(self):
#         self.mPhoneModel = 'default'
#         self.mUUID = None
#         self.mCoreVersion = None
#         self.mWeeklyLogDataFrame = DataFrame(columns=cm.FRAME_LABELS)
#         self.mIsCurrWeeklyLogDataFrame = False
#         self.mStatAnalysis = StatAnalysis()
#         self.mRateStatAnalysis = RateStatAnalysis()
#         self.mCntStatAnalysis = CntStatAnalysis()
#
#
#     # def reset(self):
#     #
#     # def getHeadInfo(self):
#     #
#     #
#     # def mergeDailyDataFrame(self,currDailyDataFrame):
#     #
#     # def getWeeklyStatistics(self):
#     # writeCSVfile(self):
#     # DIR refinedLog > Weekly > 폰별 폴더
#     # 일주일 지난 후 weekly 가 기록되면 Daily data 전 삭제
#
#
#     def getWeeklyDataFrame(self):
#         return self.mWeeklyLogDataFrame


#-----------------------------------------------------------------------------#

class CntStatAnalysis(object):

    def __init__(self):
        self.mTotalRcvdCnt = -1
        self.mEDPassCnt = -1
        self.mEDFailCnt = -1

        self.mPreambleCSPassCnt  = -1
        self.mPreambleCSFailCnt = -1

        self.mDataCSPassCnt = -1
        self.mDataCSFailCnt = -1

        self.mCRCPassCnt = -1
        self.mCRCFailCnt = -1

        self.mCRCPassCntRegBeacon = -1
        self.mCRCPassCntUnregBeacon = -1

    def setStat(self,dataframe):
        self.mTotalRcvdCnt      = dataframe.index.size
        self.mEDPassCnt         = dataframe[cm.EDPASSNAME] [ dataframe[cm.EDPASSNAME] == True ].size
        self.mPreambleCSPassCnt = dataframe[cm.PCSPASSNAME][ dataframe[cm.PCSPASSNAME] == True ].size
        self.mDataCSPassCnt     = dataframe[cm.DCSPASSNAME][ dataframe[cm.DCSPASSNAME] == True ].size
        self.mCRCPassCnt        = dataframe[cm.CRCPASSNAME][ dataframe[cm.CRCPASSNAME] == True].size

        self.mEDFailCnt         = self.mTotalRcvdCnt        - self.mEDPassCnt
        self.mPreambleCSFailCnt = self.mEDPassCnt           - self.mPreambleCSPassCnt
        self.mDataCSFailCnt     = self.mPreambleCSPassCnt   - self.mDataCSPassCnt
        self.mCRCFailCnt        = self.mDataCSPassCnt       - self.mCRCPassCnt

        self.mCRCPassCntRegBeacon = dataframe[ (dataframe.isCRCPass == True) &
                                    (dataframe.isValidBeaconID == True)].size / dataframe.columns.size
        self.mCRCPassCntUnregBeacon = dataframe[ (dataframe.isCRCPass == True) &
                                    (dataframe.isValidBeaconID == False)].size / dataframe.columns.size

    def reset(self):
        self.mTotalRcvdCnt = -1
        self.mEDPassCnt = -1
        self.mEDFailCnt = -1

        self.mPreambleCSPassCnt  = -1
        self.mPreambleCSFailCnt = -1

        self.mDataCSPassCnt = -1
        self.mDataCSFailCnt = -1

        self.mCRCPassCnt = -1
        self.mCRCFailCnt = -1

        self.mCRCPassCntRegBeacon = -1
        self.mCRCPassCntUnregBeacon = -1


class StatAnalysis(object):

    def __init__(self):
        self.mEDPassStat = EDStat()
        self.mEDfailStat = EDStat()

        self.mChannelStat = ChannelStat()

        self.mPCSPassStat = pCSStat()
        self.mPCSfailStat = pCSStat()

        self.mDCSPassStat = dCSStat()
        self.mDCSfailStat = dCSStat()

    def setStat(self,dataframe):
        self.mEDPassStat.mEDTydB_samples    = pd.to_numeric(dataframe[cm.EDTyDBNAME]
                                                            [ dataframe[cm.EDPASSNAME] == True])
        self.mEDPassStat.mEDSNRdB_samples   = pd.to_numeric(dataframe[cm.EDSNRNAME]
                                                            [ dataframe[cm.EDPASSNAME] == True])
        self.mEDfailStat.mEDTydB_samples    = pd.to_numeric(dataframe[cm.EDTyDBNAME]
                                                            [ dataframe[cm.EDPASSNAME] == False])
        self.mEDfailStat.mEDSNRdB_samples   = pd.to_numeric(dataframe[cm.EDSNRNAME]
                                                            [ dataframe[cm.EDPASSNAME] == False])

        self.mPCSPassStat.mPreambleJCsMar_sample =  pd.to_numeric(dataframe[cm.PCSJMARNAME]
                                                                  [ dataframe[cm.PCSPASSNAME] == True])
        self.mPCSfailStat.mPreambleJCsMar_sample =  pd.to_numeric(dataframe[cm.PCSJMARNAME]
                                                                  [ dataframe[cm.PCSPASSNAME] == False ])

        self.mDCSPassStat.mDataJCsParGeqCounter_samples         = pd.to_numeric(dataframe[cm.DCSPARGEQCntNAME]
                                                                                [ dataframe[cm.DCSPASSNAME] == True])
        self.mDCSPassStat.mDataJCsParRatioGeqCounter_samples    = pd.to_numeric(dataframe[cm.DCSPARRATIOGEQCntNAME]
                                                                                [ dataframe[cm.DCSPASSNAME] == True])
        self.mDCSfailStat.mDataJCsParGeqCounter_samples         = pd.to_numeric(dataframe[cm.DCSPARGEQCntNAME]
                                                                                [ dataframe[cm.DCSPASSNAME] == False])
        self.mDCSfailStat.mDataJCsParRatioGeqCounter_samples    = pd.to_numeric(dataframe[cm.DCSPARRATIOGEQCntNAME]
                                                                                [ dataframe[cm.DCSPASSNAME] == False])

        self.mChannelStat.mRicianKfactordB_samples              = pd.to_numeric(dataframe[cm.RICIANKFACTORNAME]
                                                                                [ dataframe[cm.PCSPASSNAME] == False])
        self.mChannelStat.mSpreadingTimeSec_samples             = pd.to_numeric(dataframe[cm.SPREADINGTIMENAME]
                                                                                [ dataframe[cm.PCSPASSNAME] == False])

    def reset(self):
        self.mEDPassStat = EDStat()
        self.mEDfailStat = EDStat()

        self.mChannelStat = ChannelStat()

        self.mPCSPassStat = pCSStat()
        self.mPCSfailStat = pCSStat()

        self.mDCSPassStat = dCSStat()
        self.mDCSfailStat = dCSStat()


class RateStatAnalysis(object):

    def __init__(self):
        self.mLogRcvdRate = -1.0
        self.mLogFalseAlarmRate = -1.0

        self.mPCSRcvdRate = -1.0
        self.mPCSFalseAlarmRate = -1.0

        self.mDCSRcvdRate = -1.0
        self.mDCSFalseAlarmRate = -1.0

        self.mAvgRicianKfactordB = False
        self.mAvgSpreadingTimeSec = False

        self.mNLos = -1.0
        self.mNNlos = -1.0

    def reset(self):
        self.mLogRcvdRate = -1.0
        self.mLogFalseAlarmRate = -1.0

        self.mPCSRcvdRate = -1.0
        self.mPCSFalseAlarmRate = -1.0

        self.mDCSRcvdRate = -1.0
        self.mDCSFalseAlarmRate = -1.0

        self.mAvgRicianKfactordB = False
        self.mAvgSpreadingTimeSec = False

        self.mNLos = -1.0
        self.mNNlos = -1.0

    def setStat(self,cntstat, stat):

        EDpassExceptUnregBeaconNum = max(cntstat.mEDPassCnt - cntstat.mCRCPassCntUnregBeacon,0)
        EDpassExceptRegBeaconNum   = max(cntstat.mEDPassCnt - cntstat.mCRCPassCntRegBeacon,0)

        PCSpassExceptUnregBeaconNum = max(cntstat.mPreambleCSPassCnt - cntstat.mCRCPassCntUnregBeacon,0)
        PCSpassExceptRegBeaconNum   = max(cntstat.mPreambleCSPassCnt - cntstat.mCRCPassCntRegBeacon,0)

        # mLogRcvdRate
        if ( cntstat.mCRCPassCnt > 0) and (EDpassExceptUnregBeaconNum > 0):
            self.mLogRcvdRate       =   cntstat.mCRCPassCntRegBeacon / EDpassExceptUnregBeaconNum * 100.0
        else:
            self.mLogRcvdRate = -1.0

        # mLogFalseAlarmRate
        if ( cntstat.mCRCPassCnt > 0) and (EDpassExceptRegBeaconNum > 0):
            self.mLogFalseAlarmRate =   cntstat.mCRCPassCntUnregBeacon / EDpassExceptRegBeaconNum  * 100.0
        else:
            self.mLogFalseAlarmRate = -1.0


        # mPreambleCSPassCnt
        if (cntstat.mPreambleCSPassCnt > 0) and (EDpassExceptUnregBeaconNum > 0):
            self.mPCSRcvdRate       =   (cntstat.mPreambleCSPassCnt - cntstat.mCRCPassCntUnregBeacon) / EDpassExceptUnregBeaconNum * 100.0
        else:
            self.mPCSRcvdRate = -1.0


        # mPCSFalseAlarmRate
        if (cntstat.mPreambleCSPassCnt > 0) and (EDpassExceptRegBeaconNum > 0):
            self.mPCSFalseAlarmRate = (cntstat.mPreambleCSPassCnt - cntstat.mCRCPassCntRegBeacon) / EDpassExceptRegBeaconNum * 100.0
        else:
            self.mPCSFalseAlarmRate = -1.0


        if PCSpassExceptUnregBeaconNum > 0:
            self.mDCSRcvdRate       =   (cntstat.mDataCSPassCnt - cntstat.mCRCPassCntUnregBeacon) / PCSpassExceptUnregBeaconNum * 100.0
        else:
            self.mDCSRcvdRate       = -1.0

        if PCSpassExceptRegBeaconNum > 0:
            self.mDCSFalseAlarmRate =   (cntstat.mDataCSPassCnt - cntstat.mCRCPassCntRegBeacon) / PCSpassExceptRegBeaconNum * 100.0
        else:
            self.mDCSFalseAlarmRate = -1.0


        self.mNLos                  = len(stat.mChannelStat.mRicianKfactordB_samples[
                                              stat.mChannelStat.mRicianKfactordB_samples == float('Inf')])
        self.mNNlos                 = len(stat.mChannelStat.mRicianKfactordB_samples[
                                              stat.mChannelStat.mRicianKfactordB_samples == -float('Inf')])

        chNum =                max(len(stat.mChannelStat.mRicianKfactordB_samples) - self.mNLos - self.mNNlos,0)

        if chNum > 0:
            self.mAvgRicianKfactordB    = sum(stat.mChannelStat.mRicianKfactordB_samples
                                          [(stat.mChannelStat.mRicianKfactordB_samples != float('Inf')) &
                                           (stat.mChannelStat.mRicianKfactordB_samples != -float('Inf'))]) / chNum
        else:
            self.mAvgRicianKfactordB = False


        if len(stat.mChannelStat.mSpreadingTimeSec_samples) > 0:
            self.mAvgSpreadingTimeSec   = sum(stat.mChannelStat.mSpreadingTimeSec_samples) /\
                                            len(stat.mChannelStat.mSpreadingTimeSec_samples)
        else:
            self.mAvgSpreadingTimeSec = False


    def getMeasureList(self):
        return [self.mLogRcvdRate, self.mLogFalseAlarmRate, self.mPCSRcvdRate,self.mPCSFalseAlarmRate,\
                self.mDCSRcvdRate, self.mDCSFalseAlarmRate, self.mAvgRicianKfactordB, self.mNLos, self.mNNlos,\
                self.mAvgSpreadingTimeSec]


    def display(self):
        print '# [DailyLogAnalysisWorker] ----------------------------'
        print '   Log Rcvd Rate = %2.2f%%' % self.mLogRcvdRate
        print '   Log False-alarm Rate = %2.5f%%' % self.mLogFalseAlarmRate
        print '    - - -'
        print '   pCS true-pos. Rate = %2.2f%%' % self.mPCSRcvdRate
        print '   pCS false-pos. Rate = %2.2f%%' % self.mPCSFalseAlarmRate
        print '    - - -'
        print '   dCS true-pos. Rate = %2.2f%%' % self.mDCSRcvdRate
        print '   dCS false-pos. Rate = %2.2f%%' % self.mDCSFalseAlarmRate
        print '    - - -'
        print '   Average RicianKfactor = %.2f dB' % self.mAvgRicianKfactordB
        print '   # of LOS RicianKfactor (inf) samples = %d' % self.mNLos
        print '   # of NLOS-only RicianKfactor (-inf) samples = %d' % self.mNNlos
        print '    - - -'
        print '   Average SpreadingTime = %.6f sec' % self.mAvgSpreadingTimeSec
        print '# [DailyLogAnalysisWorker] ----------------------------'

class EDStat(object):
    def __init__(self):
        self.mEDTydB_samples = Series()
        self.mEDSNRdB_samples = Series()


class ChannelStat(object):
    def __init__(self):
        self.mRicianKfactordB_samples = Series()
        self.mSpreadingTimeSec_samples = Series()


class dCSStat(object):
    def __init__(self):
        self.mDataJCsParGeqCounter_samples = Series()
        self.mDataJCsParRatioGeqCounter_samples = Series()

class pCSStat(object):
    def __init__(self):
        self.mPreambleJCsMar_sample = Series()



