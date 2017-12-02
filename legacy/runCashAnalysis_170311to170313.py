#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runDailyLogAnalysis.py
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

import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import datetime
import matplotlib.pyplot as plt
import matplotlib as matplot

IsCoreLog = False
IsBeaconLog = True


IsCLiP = False
IsCashSlide = True

# Log configureation
servertype = 's3'
frameSize = -1
phoneModel = cm.ALL_TYPE_OF_PHONES

# log profiles
if IsCashSlide:
    # 캐시 슬라이드
    appname = '캐시슬라이드'
    appkey = '5e228d8d-c869-437c-ae70-8dd87b089f64'
    currdate = '20170318'
elif IsCLiP:
    # CLiP
    appname = 'CLiP'
    appkey = '6227368d-7a59-4805-a110-24b23e8c87b3'
    currdate = '20170311'




# core 로그 처리
if IsCoreLog == True:
    downCoreLogDownWorker = downlog.LogDownloader()
    downCoreLogDownWorker.setLogInfo(currdate,'core',servertype,appname,appkey,phoneModel)
    # downCoreLogDownWorker.downLogRecord()

    dailycorelogworker = genDataFrame.DailyLogWorker()
    dailycorelogworker.init(downCoreLogDownWorker.mLogInfo)
    dailycorelogworker.makeDailyLogfileList()
    dailycorelogworker.nextDailyLogFile()

    t =time.time()
    dailycorelogworker.loadDailyLog('grep')
    elapsed = time.time() - t
    print '# [runDailyLogAnalysis] Data loading time = %s' % elapsed
    # data framing

    if len(dailycorelogworker.mFileNameList) > 0:
        t =time.time()
        coreLogDailyDataFrame = dailycorelogworker.getDailyDataFrame(frameSize)
        # coreLogDailyDataFrame.sort_values(by='deviceTime')

        elapsed = time.time() - t
        print '# [runDailyLogAnalysis] Data parsing time = %s' % elapsed

    coreLogDailyDataFrame_CRCPASS = coreLogDailyDataFrame[coreLogDailyDataFrame['isCRCPass'] == True]
    coreLogDailyDataFrame_EDPASS = coreLogDailyDataFrame[coreLogDailyDataFrame['isEnergy'] == True]


    # Data analysis
    phoneModellist = set(coreLogDailyDataFrame.phoneModel)

    #
    SMG930K = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-G930K']
    SMG930K_Len            = float(len(SMG930K))
    SMG930K_isEDPASSLen    = float(len(SMG930K[SMG930K.isEnergy == True]))
    SMG930K_isCRCPASSLen      = float(len(SMG930K[SMG930K.isCRCPass == True]))
    # #
    # # print '# [runDailyLogAnalysis] SMG930K_Len = %s' % SMG930K_Len
    # # print '# [runDailyLogAnalysis] SMG930K_isEDPASSLen = %s' % SMG930K_isEDPASSLen
    # # print '# [runDailyLogAnalysis] SMG930K_isCRCPASS = %s' % SMG930K_isCRCPASSLen
    # # print '# [runDailyLogAnalysis] SMG930K ED rate = %1.4f' % ((SMG930K_isEDPASSLen-SMG930K_isCRCPASSLen)/SMG930K_Len)
    # # print '# [runDailyLogAnalysis] SMG930K CRC rate = %1.4f' % (SMG930K_isCRCPASSLen/SMG930K_isEDPASSLen)
    # # print '#----------------------------------------------------------------'
    #
    #
    SMG930S= coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-G930S']
    SMG930S_Len            = float(len(SMG930S))
    SMG930S_isEDPASSLen    = float(len(SMG930S[SMG930S.isEnergy == True]))
    SMG930S_isCRCPASSLen      = float(len(SMG930S[SMG930S.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] SMG930S_Len = %s' % SMG930S_Len
    # print '# [runDailyLogAnalysis] SMG930S_isEDPASSLen = %s' % SMG930S_isEDPASSLen
    # print '# [runDailyLogAnalysis] SMG930S_isCRCPASS = %s' % SMG930S_isCRCPASSLen
    # print '# [runDailyLogAnalysis] SMG930S ED rate = %1.4f' % ((SMG930S_isEDPASSLen-SMG930S_isCRCPASSLen)/SMG930S_Len)
    # print '# [runDailyLogAnalysis] SMG930S CRC rate = %1.4f' % (SMG930S_isCRCPASSLen/SMG930S_isEDPASSLen)
    # print '#----------------------------------------------------------------'


    SMG850K= coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-G850K']
    SMG850K_Len            = float(len(SMG850K))
    SMG850K_isEDPASSLen    = float(len(SMG850K[SMG850K.isEnergy == True]))
    SMG850K_isCRCPASSLen      = float(len(SMG850K[SMG850K.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] SMG850K_Len = %s' % SMG850K_Len
    # print '# [runDailyLogAnalysis] SMG850K_isEDPASSLen = %s' % SMG850K_isEDPASSLen
    # print '# [runDailyLogAnalysis] SMG850K_isCRCPASS = %s' % SMG850K_isCRCPASSLen
    # print '# [runDailyLogAnalysis] SMG850K ED rate = %1.4f' % ((SMG850K_isEDPASSLen-SMG850K_isCRCPASSLen)/SMG850K_Len)
    # print '# [runDailyLogAnalysis] SMG850K CRC rate = %1.4f' % (SMG850K_isCRCPASSLen/SMG850K_isEDPASSLen)
    # print '#----------------------------------------------------------------'
#


    SMG915S= coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-G915S']
    SMG915S_Len            = float(len(SMG915S))
    SMG915S_isEDPASSLen    = float(len(SMG915S[SMG915S.isEnergy == True]))
    SMG915S_isCRCPASSLen      = float(len(SMG915S[SMG915S.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] SMG915S_Len = %s' % SMG915S_Len
    # print '# [runDailyLogAnalysis] SMG915S_isEDPASSLen = %s' % SMG915S_isEDPASSLen
    # print '# [runDailyLogAnalysis] SMG915S_isCRCPASS = %s' % SMG915S_isCRCPASSLen
    # print '# [runDailyLogAnalysis] SMG915S ED rate = %1.4f' % ((SMG915S_isEDPASSLen-SMG915S_isCRCPASSLen)/SMG915S_Len)
    # print '# [runDailyLogAnalysis] SMG915S CRC rate = %1.4f' % (SMG915S_isCRCPASSLen/SMG915S_isEDPASSLen)
    # print '#----------------------------------------------------------------'
    #



    SMG935S = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-G935S']
    SMG935S_Len            = float(len(SMG935S))
    SMG935S_isEDPASSLen    = float(len(SMG935S[SMG935S.isEnergy == True]))
    SMG935S_isCRCPASSLen      = float(len(SMG935S[SMG935S.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] SMG935S_Len = %s' % SMG935S_Len
    # print '# [runDailyLogAnalysis] SMG935S_isEDPASSLen = %s' % SMG935S_isEDPASSLen
    # print '# [runDailyLogAnalysis] SMG935S_isCRCPASS = %s' % SMG935S_isCRCPASSLen
    # print '# [runDailyLogAnalysis] SMG935S ED rate = %1.4f' % ((SMG935S_isEDPASSLen-SMG935S_isCRCPASSLen)/SMG935S_Len)
    # print '# [runDailyLogAnalysis] SMG935S CRC rate = %1.4f' % (SMG935S_isCRCPASSLen/SMG935S_isEDPASSLen)
    # print '#----------------------------------------------------------------'
    #
    VIEL90  = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='VIE-L09']
    VIEL90_Len            = float(len(VIEL90))
    VIEL90_isEDPASSLen    = float(len(VIEL90[VIEL90.isEnergy == True]))
    VIEL90_isCRCPASSLen      = float(len(VIEL90[VIEL90.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] VIEL90_Len = %s' % VIEL90_Len
    # print '# [runDailyLogAnalysis] VIEL90_isEDPASSLen = %s' % VIEL90_isEDPASSLen
    # print '# [runDailyLogAnalysis] VIEL90_isCRCPASS = %s' % VIEL90_isCRCPASSLen
    # print '# [runDailyLogAnalysis] VIEL90 ED rate = %1.4f' % ((VIEL90_isEDPASSLen-VIEL90_isCRCPASSLen)/VIEL90_Len)
    # print '# [runDailyLogAnalysis] VIEL90 CRC rate = %1.4f' % (VIEL90_isCRCPASSLen/VIEL90_isEDPASSLen)
    # print '#----------------------------------------------------------------'
    #
    LGF800K = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='LG-F800K']
    LGF800K_Len            = float(len(LGF800K))
    LGF800K_isEDPASSLen    = float(len(LGF800K[LGF800K.isEnergy == True]))
    LGF800K_isCRCPASSLen      = float(len(LGF800K[LGF800K.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] LGF800K_Len = %s' % LGF800K_Len
    # print '# [runDailyLogAnalysis] LGF800K_isEDPASSLen = %s' % LGF800K_isEDPASSLen
    # print '# [runDailyLogAnalysis] LGF800K_isCRCPASS = %s' % LGF800K_isCRCPASSLen
    # print '# [runDailyLogAnalysis] LGF800K ED rate = %1.4f' % ((LGF800K_isEDPASSLen-LGF800K_isCRCPASSLen)/LGF800K_Len)
    # print '# [runDailyLogAnalysis] LGF800K CRC rate = %1.4f' % (LGF800K_isCRCPASSLen/LGF800K_isEDPASSLen)
    # print '#----------------------------------------------------------------'
    #

    LGF410S = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='LG-F410S']
    LGF410S_Len            = float(len(LGF410S))
    LGF410S_isEDPASSLen    = float(len(LGF410S[LGF410S.isEnergy == True]))
    LGF410S_isCRCPASSLen      = float(len(LGF410S[LGF410S.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] LGF410S_Len = %s' % LGF410S_Len
    # print '# [runDailyLogAnalysis] LGF410S_isEDPASSLen = %s' % LGF410S_isEDPASSLen
    # print '# [runDailyLogAnalysis] LGF410S_isCRCPASS = %s' % LGF410S_isCRCPASSLen
    # print '# [runDailyLogAnalysis] LGF410S ED rate = %1.4f' % ((LGF410S_isEDPASSLen-LGF410S_isCRCPASSLen)/LGF410S_Len)
    # print '# [runDailyLogAnalysis] LGF410S CRC rate = %1.4f' % (LGF410S_isCRCPASSLen/LGF410S_isEDPASSLen)
    # print '#----------------------------------------------------------------'

    Nex5X = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='Nexus 5X']
    Nex5X_Len            = float(len(Nex5X))
    Nex5X_isEDPASSLen    = float(len(Nex5X[Nex5X.isEnergy == True]))
    Nex5X_isCRCPASSLen      = float(len(Nex5X[Nex5X.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] Nex5X_Len = %s' % Nex5X_Len
    # print '# [runDailyLogAnalysis] Nex5X_isEDPASSLen = %s' % Nex5X_isEDPASSLen
    # print '# [runDailyLogAnalysis] Nex5X_isCRCPASS = %s' % Nex5X_isCRCPASSLen
    # print '# [runDailyLogAnalysis] Nex5X ED rate = %1.4f' % ((Nex5X_isEDPASSLen-Nex5X_isCRCPASSLen)/Nex5X_Len)
    # print '# [runDailyLogAnalysis] Nex5X CRC rate = %1.4f' % (Nex5X_isCRCPASSLen/Nex5X_isEDPASSLen)
    # print '#----------------------------------------------------------------'

    SHVE210L = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SHV-E210L']
    SHVE210L_Len            = float(len(SHVE210L))
    SHVE210L_isEDPASSLen    = float(len(SHVE210L[SHVE210L.isEnergy == True]))
    SHVE210L_isCRCPASSLen      = float(len(SHVE210L[SHVE210L.isCRCPass == True]))
    # print '# [runDailyLogAnalysis] SHVE210L_Len = %s' % SHVE210L_Len
    # print '# [runDailyLogAnalysis] SHVE210L_isEDPASSLen = %s' % SHVE210L_isEDPASSLen
    # print '# [runDailyLogAnalysis] SHVE210L_isCRCPASS = %s' % SHVE210L_isCRCPASSLen
    # print '# [runDailyLogAnalysis] SHVE210L ED rate = %1.4f' % ((SHVE210L_isEDPASSLen-SHVE210L_isCRCPASSLen)/SHVE210L_Len)
    # print '# [runDailyLogAnalysis] SHVE210L CRC rate = %1.4f' % (SHVE210L_isCRCPASSLen/SHVE210L_isEDPASSLen)
    # print '#----------------------------------------------------------------'
    #

    SMN920K = coreLogDailyDataFrame[coreLogDailyDataFrame['phoneModel']=='SM-N920K']
    SMN920K_Len            = float(len(SMN920K))
    SMN920K_isEDPASSLen    = float(len(SMN920K[SMN920K.isEnergy == True]))
    SMN920K_isCRCPASSLen      = float(len(SMN920K[SMN920K.isCRCPass == True]))
    # # print '# [runDailyLogAnalysis] SMN920K_Len = %s' % SMN920K_Len
    # # print '# [runDailyLogAnalysis] SMN920K_isEDPASSLen = %s' % SMN920K_isEDPASSLen
    # # print '# [runDailyLogAnalysis] SMN920K_isCRCPASS = %s' % SMN920K_isCRCPASSLen
    # # print '# [runDailyLogAnalysis] SMN920K ED rate = %1.4f' % ((SMN920K_isEDPASSLen-SMN920K_isCRCPASSLen)/SMN920K_Len)
    # # print '# [runDailyLogAnalysis] SMN920K CRC rate = %1.4f' % (SMN920K_isCRCPASSLen/SMN920K_isEDPASSLen)
    # # print '#----------------------------------------------------------------'

if IsBeaconLog == True:
    # beacon 로그 처리
    logtype = 'beacon'
    downBeaconLogDownWorker = downlog.LogDownloader()
    downBeaconLogDownWorker.setLogInfo(currdate,logtype,servertype)
    downBeaconLogDownWorker.downLogRecord()

    dailybeaconlogworker = genDataFrame.DailyLogWorker()
    dailybeaconlogworker.init(logtype,currdate,appkey)
    dailybeaconlogworker.makeDailyLogfileList()
    dailybeaconlogworker.nextDailyLogFile()
    dailybeaconlogworker.loadDailyLog('json')


    # data frame generation
    if len(dailybeaconlogworker.mFileNameList) > 0:
        beaconLogDailyDataFrame = dailybeaconlogworker.getDailyDataFrame(-1)
        beaconLogDailyDataFrame.sort_values(by='deviceTime')






