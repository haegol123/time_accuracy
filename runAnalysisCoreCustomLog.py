#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runAnalysisCoreCustomLog.py
# This is for Core performance measuring from CoreLogs

# written by Soonwon Ka @ Aug 2017
#------------------------------------------------------------

import sys
from os import getcwd
from os import system
import subprocess
sys.path.insert(0, getcwd()+'/python_codes')

import os
import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as pyplot
import intro
import suppdevlist
import scipy
import scipy.stats
import argparse


# logdatelist = ['20170715']
logdatelist = [
    '20170821',\
    '20170822',\
    '20170823',\
    '20170824',\
    '20170825',\
    '20170826',\
    '20170827',\
    '20170828'
    ]

# core tag list
coretaglist = [
    'CORE_DETECTION_START',
    'CORE_DETECTION_ED_FAIL',
    'CORE_DETECTION_SUCCESS',
    'CORE_DETECTION_RESULT_ZERO',
    'CORE_DETECTION_RESULT_NONE',
    'CORE_DETECTION_RESULT_AMBIGUOUS',
    'CORE_DETECTION_RESULT_CRCERROR',
    'CORE_DETECTION_RESULT_FATALERROR',
    'CORE_DETECTION_RESULT_RECORDFAIL',
    'CORE_DETECTION_RESULT_CSFAIL',
    'CORE_DETECTION_RESULT_MIC_ERROR',
    'CORE_DETECTION_RESULT_UNKNOWN_ERROR'
]

# sdkTypeList  = [ "smarton","receiver"]
sdkTypeList  = [ "smarton"]

# get arguments from prompt
parser = argparse.ArgumentParser()
parser.add_argument('-v','--verbose', action='store_true', help='print all logs')
args = parser.parse_args()

# set the commandline print level (verbose or not)
VERBOSE = args.verbose

system('clear')


appname = 'user'
logtype = 'custom'

isPerDevAnalysis = True
isTimeLineAnalysis = False
isIDHistAnalysis = False
isPdfFitting   = True

# plot options
isPerDevPlot =False
isEdSNRPlot = False
isEdTyPlot  = False
isFreqLineDetPlot = False

# dist_names = ['gamma','beta','expon','betaprime','norm']
dist_names = ['norm','laplace','t']


analysisdate = str(datetime.date.today())
analysisdate = analysisdate[0:4] + analysisdate[5:7] + analysisdate[8:10]

CSVfile_DIR = getcwd() + '/csvfiles/dailyDataFrame/'+logtype+'/'+appname+'/'
FIGfile_DIR = getcwd() + '/fig/'+logtype+'logData/'+appname+'/' + analysisdate + '/'


if not os.path.exists(FIGfile_DIR):
    subprocess.check_call('mkdir ' + FIGfile_DIR, shell=True)

if not os.path.exists(CSVfile_DIR):
    subprocess.check_call('mkdir ' + CSVfile_DIR, shell=True)


# subprocess.check_call('mkdir ' + getcwd() + '/fig/'+logtype+'logData', shell=True)
# subprocess.check_call('mkdir ' + getcwd() + '/fig/'+logtype+'logData/'+appname, shell=True)

intro.intro_CustomLogAnalysis()


print '# [runAnalysisCoreCustomLog] Configration'
print '# [runAnalysisCoreCustomLog] isPerDevAnalysis = %s' % isPerDevAnalysis
print '# [runAnalysisCoreCustomLog] isTimeLineAnalysis = %s' % isTimeLineAnalysis
print '# [runAnalysisCoreCustomLog] isIDHistAnalysis = %s' % isIDHistAnalysis

dfEntire        = DataFrame()
dfValidBeacon  = DataFrame()
dfInValidBeacon = DataFrame()


for i in range(0, len(logdatelist)):
    logdate = logdatelist[i]

    csvfilename = CSVfile_DIR + logdate + '_'+logtype+'Log_'+appname+'_DailyDataFrame.csv'

    print '# [runAnalysisCoreCustomLog] Loading data from %s' % csvfilename

    curr_dataframe = pd.read_csv(csvfilename)


    if not(curr_dataframe.empty):

        dfEntire = pd.concat([dfEntire, curr_dataframe],ignore_index=True)
        edPassCount = float(len(curr_dataframe[curr_dataframe.coreTag =='CORE_DETECTION_START']) - \
                            len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_MIC_ERROR']) - \
                            len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_ED_FAIL']))
        prCsPassCount = float(edPassCount - \
                              len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_NONE']) - \
                              len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_AMBIGUOUS']))
        # prCsPassCount2 = float(edPassCount - \
        #       len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_NONE']) - \
        #       len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_AMBIGUOUS']) - \
        #       len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_CSFAIL']))
        fatalErrCount = float(len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_FATALERROR']))
        crcErrCount = float(len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_CRCERROR']))
        beaconCount = float(len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_SUCCESS']) + \
                            len(curr_dataframe[curr_dataframe.coreTag == 'CORE_DETECTION_RESULT_ZERO']))

        if VERBOSE:
            print '# -- CORE TAG STAT for %s ----------------------------'
            for ii in range(0,len(coretaglist)):
                print '# [runAnalysisCoreCustomLog] for %s    = %d'\
                      % (coretaglist[ii], len(curr_dataframe[curr_dataframe.coreTag == coretaglist[ii]]))

        print '# -- DAILY REPORT for %s -----------------------------' % logdate
        print '# [runAnalysisCoreCustomLog] edPass count     = %d' % edPassCount
        print '# [runAnalysisCoreCustomLog] prCsPass count   = %d' % prCsPassCount
        # print '# [runAnalysisCoreCustomLog] prCsPass count2 = %d' % prCsPassCount2
        print '# [runAnalysisCoreCustomLog] fatalErr count   = %d' % fatalErrCount
        print '# [runAnalysisCoreCustomLog] crcErr count     = %d' % crcErrCount
        print '# ----------------------------------------------------------'
        print '# [runAnalysisCoreCustomLog] beacon count     = %d' % beaconCount
        print '# ----------------------------------------------------------'

print '# [runAnalysisCoreCustomLog] csv loading done!'
dfEntire = dfEntire.reindex()
# dfEdNoisedB = -1.0 * (dfEntire.edSNRdB - dfEntire.edTy)
# dfEdNoisedB = DataFrame(data=dfEdNoisedB, columns= ['edNoisedB'])
# dfEntire = pd.concat([dfEntire,dfEdNoisedB ],axis=1)

# dfInValidBeacon = dfEntire[ dfEntire['isValidBeaconID'] == False]
# dfValidBeacon   = dfEntire[ dfEntire['isValidBeaconID'] == True ]
#
# dfInValidBeacon = dfInValidBeacon.reindex()
# dfValidBeacon   = dfValidBeacon.reindex()

print '# -------------------------------------------------------------------------------------- '
print '# [runAnalysisCoreCustomLog] log collecting period = %s' % logdatelist
# print '# [runAnalysisCoreCustomLog] Total Invalid count = %s' % dfInValidBeacon.phoneModel.size

for k in range(0,len(sdkTypeList)):
    # classification of receiver and smarton data
    currSdkType = sdkTypeList[k]

#    currFIGfile_DIR = FIGfile_DIR + currSdkType + '/'
#    subprocess.check_call('mkdir '+currFIGfile_DIR, shell=True)

    dfEntire_curr        = dfEntire         [dfEntire.sdkType.str.contains(currSdkType)]

    # dfValidBeacon_curr   = dfValidBeacon    [dfValidBeacon.sdkType.str.contains(currSdkType)]
    # dfInValidBeacon_curr = dfInValidBeacon  [dfInValidBeacon.sdkType.str.contains(currSdkType)]

    print '# -------------------------------------------------------------------------------------- '
    print '# [runAnalysisCoreCustomLog] sdkType = %s' % currSdkType
    # print '# [runAnalysisCoreCustomLog] Total Invalid count = %s' % dfInValidBeacon_curr.phoneModel.size
    detectionLogCount = len(dfEntire_curr[dfEntire_curr.detection==True])
    coreRcvTrialCount = len(dfEntire_curr[dfEntire_curr.coreTag=='CORE_DETECTION_START'])

    edPassCount = float(len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_START']) - \
                            len(dfEntire[dfEntire.coreTag == 'CORE_DETECTION_RESULT_MIC_ERROR']) - \
                        len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_ED_FAIL']))
    prCsPassCount = float(edPassCount - \
                          len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_NONE']) - \
                          len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_AMBIGUOUS']))
    crcErrCount = float(len(dfEntire_curr[dfEntire_curr.coreTag=='CORE_DETECTION_RESULT_CRCERROR']))
    beaconCount = float(len(dfEntire_curr[dfEntire_curr.coreTag=='CORE_DETECTION_SUCCESS']) + \
                  len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_ZERO']))


    print '# -------------------------------------------------------------------------------------- '

    print '# [runAnalysisCoreCustomLog] detectionLogCount  = %d' % detectionLogCount
    print '# [runAnalysisCoreCustomLog] coreRcvTrialCount  = %d' % coreRcvTrialCount
    print '# [runAnalysisCoreCustomLog] edPassCount        = %d' % edPassCount
    print '# [runAnalysisCoreCustomLog] prCsPassCount      = %d' % prCsPassCount
    # print '# [runAnalysisCoreCustomLog] prCsPassCount2     = %d' % float(edPassCount - \
    #                       len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_NONE']) - \
    #                       len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_AMBIGUOUS']) - \
    #                       len(dfEntire_curr[dfEntire_curr.coreTag == 'CORE_DETECTION_RESULT_CSFAIL']))

    print '# [runAnalysisCoreCustomLog] crcErrCount        = %d' % crcErrCount
    print '# ----------------------------------------------------------'
    print '# [runAnalysisCoreCustomLog] beaconCount        = %d' % beaconCount
    print '# ----------------------------------------------------------'
    print '# [runAnalysisCoreCustomLog] coreRcvTrialCount / (detectionLogCount*2) = %.1f%%' % (float(coreRcvTrialCount)/(float(detectionLogCount)*2.0)*100.0)
    print '# [runAnalysisCoreCustomLog] False alarm rate   = tot beacon # / detectionLogCount    = %f%%' % (beaconCount/float(detectionLogCount)*100.0)
    print '# [runAnalysisCoreCustomLog] False alarm rate\'  = tot beacon # / coreRcvTrialCount = %f%%' % (beaconCount/float(coreRcvTrialCount)*100.0)

    #
    # if not (dfInValidBeacon_curr.empty):
    #
    #     if isPerDevAnalysis:
    #         totalLen                        = dfEntire_curr.phoneModel.size
    #         entireDevOccupancyCnt           = pd.value_counts(dfEntire_curr.phoneModel)
    #         entireDevOccupancyRatePercent          = entireDevOccupancyCnt / totalLen * 100.0
    #
    #
    #         inValidTotalLen                     = dfInValidBeacon_curr.phoneModel.size
    #         inValidDevOccupancyCnt              = pd.value_counts(dfInValidBeacon_curr.phoneModel) #
    #         validDevOccupancyCnt                = pd.value_counts(dfValidBeacon_curr.phoneModel)
    #         entireDevOccupancyCntforInvalid     = entireDevOccupancyCnt.loc[inValidDevOccupancyCnt.index] # check only for phonemodel which containing invalid beacon
    #         entireDevOccupancyCntforValid       = entireDevOccupancyCnt.loc[validDevOccupancyCnt.index] # check only for phonemodel which containing invalid beacon
    #
    #
    #         beaconErrRate        = inValidDevOccupancyCnt / entireDevOccupancyCntforInvalid
    #         beaconRcvRate        = validDevOccupancyCnt / entireDevOccupancyCntforValid
    #         beaconErrRateSupp    = beaconErrRate.loc[suppdevlist.ANDROID].to_frame()
    #         beaconRcvdRateSupp    = beaconRcvRate.loc[suppdevlist.ANDROID].to_frame()
    #
    #         beaconRcvRate        = beaconRcvRate.dropna()
    #         beaconErrRatePercent = beaconErrRate * 100.0
    #
    #         weightedBERPercent  = beaconErrRate * entireDevOccupancyRatePercent
    #         weightedBERPercent  = weightedBERPercent.dropna()
    #         weightedBERPercent  = weightedBERPercent [weightedBERPercent  > 0.05]  # plot phoneModel above 0.05%
    #
    #         if isPerDevPlot:
    #             entireDevOccupancyRateForPlot = entireDevOccupancyRatePercent[entireDevOccupancyRatePercent > 1.0]
    #             beaconErrRateForPlot = beaconErrRatePercent[beaconErrRatePercent > 5.0]  # plot phoneModel above 5%
    #
    #             hfig1 = pyplot.figure(1,figsize=(7,7))
    #             entireDevOccupancyRateForPlot.plot(kind='bar')
    #             pyplot.ylabel('Occupancy Rate (%)')
    #             pyplot.xlabel('phoneModel')
    #             pyplot.title('SdkType: '+ currSdkType + ' Occupancy Rate')
    #             hfig1.savefig(currFIGfile_DIR + analysisdate + '_phoneModelOccupancyRate.png')
    #
    #             if not(beaconErrRateForPlot.empty):
    #                 hfig2= pyplot.figure(2,figsize=(10,7))
    #                 beaconErrRateForPlot.plot(kind='bar')
    #                 pyplot.ylabel('Beacon Err Rate (%)')
    #                 pyplot.xlabel('phoneModel')
    #                 hfig2.savefig(currFIGfile_DIR + analysisdate + '_beaconErrRate.png')
    #
    #
    #             if not(weightedBERPercent.empty):
    #
    #                 hfig3 = pyplot.figure(3,figsize=(10,7))
    #                 weightedBERPercent.plot(kind='bar')
    #                 pyplot.ylabel('weigted Beacon Err Rate (%)')
    #                 pyplot.xlabel('phoneModel')
    #                 pyplot.title('weighted Beacon Err Rate')
    #                 hfig3.savefig(currFIGfile_DIR + analysisdate + '_weightedBER.png')
    #
    #
    #
    #         if isEdSNRPlot:
    #             hfig4 = pyplot.figure(4,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edSNRdB,dfCurrValidDev.freqLineMSEdB,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edSNRdB,dfCurrInvalidDev.freqLineMSEdB,color='r',marker='x')
    #                 pyplot.xlabel('edSNRdB')
    #                 pyplot.ylabel('freqLineMSEdB')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #
    #             hfig5 = pyplot.figure(5,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edSNRdB,dfCurrValidDev.freqLineSlope,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edSNRdB,dfCurrInvalidDev.freqLineSlope,color='r',marker='x')
    #                 pyplot.xlabel('edSNRdB')
    #                 pyplot.ylabel('freqLineSlope')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #
    #
    #
    #             hfig6 = pyplot.figure(6,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edSNRdB,dfCurrValidDev.edTy,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edSNRdB,dfCurrInvalidDev.edTy,color='r',marker='x')
    #                 pyplot.xlabel('edSNRdB')
    #                 pyplot.ylabel('edTy')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #             hfig4.savefig(currFIGfile_DIR + analysisdate + '_edSNRdBvsfreqLineMSEdB.png')
    #             hfig5.savefig(currFIGfile_DIR + analysisdate + '_edSNRdBvsfreqLineSlope.png')
    #             hfig6.savefig(currFIGfile_DIR + analysisdate + '_edSNRdBcvsedTy.png')
    #
    #
    #
    #             hfig15 = pyplot.figure(15,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edNoisedB,dfCurrValidDev.edTy,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edNoisedB,dfCurrInvalidDev.edTy,color='r',marker='x')
    #                 pyplot.xlabel('edNoisedB')
    #                 pyplot.ylabel('edTy')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #             hfig15.savefig(currFIGfile_DIR + analysisdate + '_edNoisedBcvsedTy.png')
    #
    #
    #
    #         if isFreqLineDetPlot:
    #             hfig11 = pyplot.figure(11,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.freqLineMSEdB,dfCurrValidDev.freqLineSlope,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.freqLineMSEdB,dfCurrInvalidDev.freqLineSlope,color='r',marker='x')
    #                 pyplot.xlabel('freqLineMSEdB')
    #                 pyplot.ylabel('freqLineSlope')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #             hfig11.savefig(currFIGfile_DIR + analysisdate + '_freqLineMSEdBvsfreqLineSlope.png')
    #
    #
    #         if isPdfFitting:
    #
    #             # resolution = 5000
    #             # xmin = 0
    #             # xmax = 5000
    #             # xrange = [xmin,xmax]
    #             # hist_resol = np.linspace(xmin,xmax,resolution)
    #             # pdf_resol = np.linspace(xmin, xmax, xmax)
    #             # --------------------------
    #             xmindB = -20
    #             xmaxdB = 35
    #             resolution = xmaxdB -xmindB
    #
    #             xrangedB = [xmindB,xmaxdB]
    #             hist_resol = np.linspace(xmindB,xmaxdB ,resolution)
    #             pdf_resol  = np.linspace(xmindB, xmaxdB , resolution)
    #             # --------------------------
    #
    #
    #             checkPhoneList = weightedBERPercent.index
    #
    #             hfig12 = pyplot.figure(12,figsize=(40,10))
    #             for j in range(0,len(checkPhoneList)):
    #                 currDev = checkPhoneList[j]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 # y                =  np.power(10,dfCurrValidDev.edSNRdB.values/10)
    #                 # y                =  y[ y < xmax]
    #
    #                 #--------------------------
    #                 y                =  dfCurrValidDev.edSNRdB.values
    #                 y                =  y[ y > xmindB]
    #                 y                =  y[ y < xmaxdB]
    #                 #--------------------------
    #
    #                 fittedPdfSize = y.size
    #                 histWeight = np.ones_like(y) / float(fittedPdfSize)
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.hist(y,hist_resol,weights=histWeight)
    #                 pyplot.title(currDev)
    #
    #                 # pdf fitting
    #                 for dist_name in dist_names:
    #                     dist = getattr(scipy.stats, dist_name)
    #                     param = dist.fit(y)
    #                     pdf_fitted = dist.pdf(pdf_resol, *param[:-2],loc=param[-2],  scale=param[-1])
    #                     pyplot.plot(pdf_resol,pdf_fitted, label=dist_name)
    #                 #--------------------------
    #                 pyplot.xlim([xmindB,xmaxdB])
    #                 #--------------------------
    #
    #                 pyplot.xlabel('edSNRdB')
    #                 pyplot.legend(loc='upper right')
    #             hfig12.savefig(currFIGfile_DIR + analysisdate + '_edSNR_Valid_Hist.png')
    #
    #
    #             hfig17 = pyplot.figure(17, figsize=(40, 10))
    #             for j in range(0, len(checkPhoneList)):
    #                 currDev = checkPhoneList[j]
    #                 dfCurrInvalidDev = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 # y                =  np.power(10,dfCurrInvalidDev.edSNRdB.values/10)
    #                 # y                =  y[ y < xmax]
    #
    #                 #--------------------------
    #                 y                =  dfCurrInvalidDev.edSNRdB.values
    #                 y                =  y[ y > xmindB]
    #                 y                =  y[ y < xmaxdB]
    #                 #--------------------------
    #
    #                 fittedPdfSize = y.size
    #                 histWeight = np.ones_like(y) / float(fittedPdfSize)
    #
    #
    #                 pyplot.subplot(2,int(round(len(checkPhoneList)/2.0)),j+1)
    #                 pyplot.hist(y,hist_resol,weights=histWeight)
    #                 pyplot.title(currDev)
    #
    #                 # pdf fitting
    #                 for dist_name in dist_names:
    #                     dist = getattr(scipy.stats, dist_name)
    #                     param = dist.fit(y)
    #                     pdf_fitted = dist.pdf(pdf_resol, *param[:-2],loc=param[-2], scale=param[-1])
    #                     pyplot.plot(pdf_resol,pdf_fitted, label=dist_name)
    #                 #--------------------------
    #                 pyplot.xlim([xmindB,xmaxdB])
    #                 #--------------------------
    #
    #                 # pyplot.xlim([xmin,15])
    #                 pyplot.xlabel('edSNRdB')
    #                 pyplot.legend(loc='upper right')
    #             hfig17.savefig(currFIGfile_DIR + analysisdate + '_edSNR_Invalid_Hist.png')
    #
    #
    #         if isEdTyPlot:
    #             hfig7 = pyplot.figure(7,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edTy,dfCurrValidDev.freqLineMSEdB,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edTy,dfCurrInvalidDev.freqLineMSEdB,color='r',marker='x')
    #                 pyplot.xlabel('edTy')
    #                 pyplot.ylabel('freqLineMSEdB')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #
    #             hfig8 = pyplot.figure(8,figsize=(20,10))
    #             for j in range(0,len(weightedBERPercent.index)):
    #                 currDev = weightedBERPercent.index[j]
    #                 dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
    #                 dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
    #
    #                 pyplot.subplot(2,int(round(len(weightedBERPercent.index)/2.0)),j+1)
    #                 pyplot.scatter(dfCurrValidDev.edTy,dfCurrValidDev.freqLineSlope,color='b',marker='o')
    #                 pyplot.scatter(dfCurrInvalidDev.edTy,dfCurrInvalidDev.freqLineSlope,color='r',marker='x')
    #                 pyplot.xlabel('edTy')
    #                 pyplot.ylabel('freqLineSlope')
    #                 pyplot.title(currDev)
    #                 pyplot.legend(['Valid','Invalid'])
    #             hfig7.savefig(currFIGfile_DIR + analysisdate + '_edTyvsfreqLineMSEdB.png')
    #             hfig8.savefig(currFIGfile_DIR + analysisdate + '_edTyvsfreqLineSlope.png')
    #
    #
    #
    #
    #
    #     if isIDHistAnalysis:
    #         hfig9 = pyplot.figure(9, figsize=(10, 7))
    #         dfInValidBeacon_curr.beacon.hist(bins=40)
    #         pyplot.ylabel('Invalid Beacon Cnt')
    #         pyplot.xlabel('beacon ID')
    #         pyplot.title('Histogram distribution of Invalid Beacon ' + 'sdkType: '+ currSdkType,fontsize=16)
    #         hfig9.savefig(currFIGfile_DIR + analysisdate + '_IDHist.png')
    #
    #
    #     if isTimeLineAnalysis:
    #         dfInvalidDevTime = DataFrame(data=pd.to_datetime(dfInValidBeacon_curr['deviceTime']))
    #         dfValidDevTime = DataFrame(data=pd.to_datetime(dfValidBeacon_curr['deviceTime']))
    #
    #         dfInvalidDevTime.set_index('deviceTime', drop=False, inplace=True)
    #         dfValidDevTime.set_index('deviceTime', drop=False, inplace=True)
    #
    #         hfig10 = pyplot.figure(10,figsize=(20,5))
    #         dfInvalidDevTimeCnt = dfInvalidDevTime.groupby(pd.TimeGrouper(freq='1Min')).count()
    #         dfValidDevTimeCnt = dfValidDevTime.groupby(pd.TimeGrouper(freq='1Min')).count()
    #
    #         # pyplot.subplot(2,1,1)
    #         pyplot.plot(dfValidDevTimeCnt.index,dfValidDevTimeCnt/dfValidDevTimeCnt.sum(),color='b')
    #         pyplot.plot(dfInvalidDevTimeCnt.index,dfInvalidDevTimeCnt/dfInvalidDevTimeCnt.sum(),color='r')
    #         pyplot.xlabel('datetime',fontsize=16)
    #         pyplot.ylabel('Beacon Cnt over time lines')
    #         pyplot.legend(['Valid','Invalid'])
    #         pyplot.show()
    #
    #         hfig10.savefig(currFIGfile_DIR + analysisdate + '_timeLineAnalysis.png')
    #
    #
    # else:
    #     print '# [runAnalysisDetectLog] No Invalid Beacon for %s' % currSdkType


