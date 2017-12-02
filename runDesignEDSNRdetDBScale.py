#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runDesignEDSNRdet.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------

import sys
from os import getcwd
from os import system
import subprocess
sys.path.insert(0, getcwd()+'/python_codes')

import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import intro
import suppdevlist
import scipy
import scipy.stats
import matplotlib.pyplot as pyplot


# logdatelist = ['20170715']
logdatelist = ['20170701',\
               '20170702',\
               '20170703',\
               '20170704',\
               '20170707',\
               '20170708',\
               '20170709',\
               '20170713',\
               '20170714',\
               '20170715',\
               '20170716',\
               '20170717',\
               '20170718',\
               '20170719',\
               '20170720',\
               '20170721',\
               '20170722',\
               '20170723'
               ]

# modelingList
modelinglist = ['norm','laplace','t']
modelingNameList = ['Norm', 'Laplace', 'StudentT']

modelinglist_curr = modelinglist[2]
modelingNameList_curr = modelingNameList[2]

# app client
appclientlist = ['clip', 'cash']

appclient_curr = appclientlist[0]


# sdkTypeList  = [ "smarton","receiver"]
sdkTypeList  = [ "smarton"]

system('clear')

isPerDevAnalysis = True
isEDSNRdetRulePlot = False
isEDSNRperformanceResult = True

ValidBayesCost   = 0.1
InvalidBayesCost = 1.0 - ValidBayesCost

analysisdate = str(datetime.date.today())
analysisdate = analysisdate[0:4] + analysisdate[5:7] + analysisdate[8:10]

CSVfile_DIR = getcwd() + '/csvfiles/dailyDataFrame/detect/'+appclient_curr+'/'
ANAfile_DIR = getcwd() + '/csvfiles/analysisResult/'+ appclient_curr+'/' + analysisdate + '/'
FIGfile_DIR = getcwd() + '/fig/detectlogData/' + appclient_curr+'/' + analysisdate + '/'


subprocess.call('mkdir ' + CSVfile_DIR, shell=True)
subprocess.call('mkdir ' + ANAfile_DIR, shell=True)
subprocess.call('mkdir ' + FIGfile_DIR, shell=True)

intro.intro_DesignEDSNRdet()


print '# [runDesignEDSNRdetDBScale] Configration'
print '# [runDesignEDSNRdetDBScale] isPerDevAnalysis = %s' % isPerDevAnalysis
print '# [runDesignEDSNRdetDBScale] isEDSNRdetRulePlot = %s' % isEDSNRdetRulePlot


dfEntire        = DataFrame()
dfValidBeacon  = DataFrame()
dfInValidBeacon = DataFrame()


for i in range(0, len(logdatelist)):
    logdate = logdatelist[i]

    csvfilename = CSVfile_DIR + logdate + '_detectLog_'+appclient_curr+'_DailyDataFrame.csv'

    print '# [runDesignEDSNRdetDBScale] Loading data from %s' % csvfilename

    curr_dataframe = pd.read_csv(csvfilename)

    if not(curr_dataframe.empty):
        dfEntire = pd.concat([dfEntire, curr_dataframe],ignore_index=True)
        print '# [runDesignEDSNRdetDBScale] beacon count of %s = %s' % (logdate, curr_dataframe.phoneModel.size)

print '# [runDesignEDSNRdetDBScale] csv loading done!'
dfEntire = dfEntire.reindex()


dfInValidBeacon = dfEntire[ dfEntire['isValidBeaconID'] == False]
dfValidBeacon   = dfEntire[ dfEntire['isValidBeaconID'] == True ]

dfInValidBeacon = dfInValidBeacon.reindex()
dfValidBeacon   = dfValidBeacon.reindex()

print '# -------------------------------------------------------------------------------------- '
print '# [runDesignEDSNRdetDBScale] log collecting period = %s' % logdatelist
print '# [runDesignEDSNRdetDBScale] Total beacon count = %s' % dfEntire.phoneModel.size
print '# [runDesignEDSNRdetDBScale] Total Invalid count = %s' % dfInValidBeacon.phoneModel.size

for k in range(0,len(sdkTypeList)):
    # classification of receiver and smarton data
    currSdkType = sdkTypeList[k]
    xmindB = -20.0
    xmaxdB = 30.0
    resolution = (xmaxdB - xmindB)*100.0

    pdf_resol = np.linspace(xmindB, xmaxdB, resolution)
    minSampleSize = 20

    checkPhoneList = suppdevlist.ANDROID

    dfEntire_curr        = dfEntire         [dfEntire.sdkType.str.contains(currSdkType)]
    dfValidBeacon_curr   = dfValidBeacon    [dfValidBeacon.sdkType.str.contains(currSdkType)]
    dfInValidBeacon_curr = dfInValidBeacon  [dfInValidBeacon.sdkType.str.contains(currSdkType)]

    print '# -------------------------------------------------------------------------------------- '
    print '# [runDesignEDSNRdetDBScale] sdkType = %s' % currSdkType
    print '# [runDesignEDSNRdetDBScale] Total beacon count = %s' % dfEntire_curr.phoneModel.size
    print '# [runDesignEDSNRdetDBScale] Total Invalid count = %s' % dfInValidBeacon_curr.phoneModel.size
    print '# [runDesignEDSNRdetDBScale] ValidBayesCost = %s' % ValidBayesCost
    print '# [runDesignEDSNRdetDBScale] pdf resolution = %1.2f dB' % ((xmaxdB - xmindB) / resolution)


    if isEDSNRdetRulePlot:
        currFIGfile_DIR = FIGfile_DIR + currSdkType + '/'
        subprocess.call('mkdir ' + currFIGfile_DIR, shell=True)

    if not (dfInValidBeacon_curr.empty):

        if isPerDevAnalysis:
            totalLen                        = dfEntire_curr.phoneModel.size
            entireDevOccupancyCnt           = pd.value_counts(dfEntire_curr.phoneModel)
            entireDevOccupancyRatePercent          = entireDevOccupancyCnt / totalLen * 100.0

            inValidTotalLen                     = dfInValidBeacon_curr.phoneModel.size
            inValidDevOccupancyCnt              = pd.value_counts(dfInValidBeacon_curr.phoneModel) #
            validDevOccupancyCnt                = pd.value_counts(dfValidBeacon_curr.phoneModel)
            entireDevOccupancyCntforInvalid     = entireDevOccupancyCnt.loc[inValidDevOccupancyCnt.index] # check only for phonemodel which containing invalid beacon
            entireDevOccupancyCntforValid       = entireDevOccupancyCnt.loc[validDevOccupancyCnt.index] # check only for phonemodel which containing invalid beacon


            beaconErrRate        = inValidDevOccupancyCnt / entireDevOccupancyCntforInvalid
            beaconRcvRate        = validDevOccupancyCnt / entireDevOccupancyCntforValid

            beaconErrRateSupp    = beaconErrRate.loc[suppdevlist.ANDROID].to_frame()
            beaconRcvdRateSupp   = beaconRcvRate.loc[suppdevlist.ANDROID].to_frame()
            beaconRcvRate        = beaconRcvRate.dropna()


            if isEDSNRdetRulePlot:
                beaconErrRatePercent = beaconErrRate * 100.0
                weightedBERPercent = beaconErrRate * entireDevOccupancyRatePercent
                weightedBERPercent = weightedBERPercent.dropna()
                weightedBERPercent = weightedBERPercent[weightedBERPercent > 0.05]  # plot phoneModel above 0.05%
                checkPhoneList = weightedBERPercent.index

            dfEDSNRDetDesign          =  pd.concat([beaconErrRateSupp, beaconRcvdRateSupp, beaconErrRateSupp/beaconRcvdRateSupp],axis=1)
            dfEDSNRDetDesign.columns   = ['Invalid Prior Rate','Valid Prior Rate','Invalid prior / Valid prior']
            dfValidStudentTParam = DataFrame(index=suppdevlist.ANDROID)#, \
#                                                  columns=['Valid '+modelingNameList_curr+' df',\
#                                                           'Valid '+modelingNameList_curr+' loc', 'Valid '+modelingNameList_curr+' scale'])

            dfInvalidStudentTParam = DataFrame(index=suppdevlist.ANDROID)#, \
#                                                    columns=['Invalid '+modelingNameList_curr+' df',\
#                                                             'Invalid '+modelingNameList_curr+' loc', 'Invalid '+modelingNameList_curr+' scale'])

            dfEDFailRangedB           = DataFrame(index=suppdevlist.ANDROID,\
                                                    columns=['gamma1','gamma2'])

            dfPerformanceResult = DataFrame(index=suppdevlist.ANDROID, \
                                        columns=['validPassRate', 'invalidFilteredRate',\
                                                 'validPassCount','validTotalCount',\
                                                 'invalidFilteredCount','invalidTotalCount'])

            if isEDSNRdetRulePlot:
                hfig1 = pyplot.figure(1,figsize=(40,10))

            for j in range(0,len(checkPhoneList)):
                currDev = checkPhoneList[j]
                if isEDSNRdetRulePlot:
                    pyplot.subplot(2, int(round(len(checkPhoneList) / 2.0)), j + 1)

                dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
                dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]
                print '# --------------------------------------------------------------------------------------'
                print '[runDesignEDSNRdetDBScale] currDev = %s' % currDev


                if dfCurrValidDev.size > minSampleSize and dfCurrInvalidDev.size > minSampleSize:

                    validPrior   = dfEDSNRDetDesign.loc[currDev]['Valid Prior Rate']
                    invalidPrior = dfEDSNRDetDesign.loc[currDev]['Invalid Prior Rate']

                    # likelihood pdf fitting for Valid
                    y                =  dfCurrValidDev.edSNRdB.values
                    y                =  y[ y > xmindB]
                    y                =  y[ y < xmaxdB]

                    if y.size < minSampleSize:
                        print '[runDesignEDSNRdetDBScale] %s has not enough data samples' % currDev
                        validhist = dfCurrValidDev.edSNRdB.values
                        validhistFiltered = validhist
                        invalidhist = dfCurrInvalidDev.edSNRdB.values

                        dfPerformanceResult.loc[currDev].validPassCount = \
                            validhistFiltered.size
                        dfPerformanceResult.loc[currDev].validTotalCount = \
                            validhist.size
                        if validhist.size == 0:
                            dfPerformanceResult.loc[currDev].validPassRate = 0
                        else:
                            dfPerformanceResult.loc[currDev].validPassRate = \
                                float(validhistFiltered.size) / float(validhist.size)
                        dfPerformanceResult.loc[currDev].invalidFilteredCount = 0
                        dfPerformanceResult.loc[currDev].invalidTotalCount = \
                            invalidhist.size
                        dfPerformanceResult.loc[currDev].invalidFilteredRate = 0

                        print 'size of validhist           = %d' % validhist.size
                        print 'size of validhistFiltered   = %d' % validhistFiltered.size
                        print ' - pass rate      = %.2f%%' % (
                            dfPerformanceResult.loc[currDev].validPassRate * 100.0)
                        print 'size of invalidhist         = %d' % invalidhist.size
                        print 'size of invalidhistFiltered = %d' % 0
                        print ' - filtering rate = %.2f%%' % (0.0 * 100.0)
                        continue

                    dist = getattr(scipy.stats, modelinglist_curr) # 't', 'norm', 'laplace'
                    validStudentTParam = dist.fit(y)
                    pdf_fitted_valid = dist.pdf(pdf_resol, *validStudentTParam[:-2], loc=validStudentTParam[-2], scale=validStudentTParam[-1])
                    posterior_pdf_valid  = pdf_fitted_valid * validPrior * ValidBayesCost


                    # likelihood pdf fitting for invalid
                    y                =  dfCurrInvalidDev.edSNRdB.values
                    y                =  y[ y > xmindB]
                    y                =  y[ y < xmaxdB]
                    if y.size < minSampleSize:
                        print '[runDesignEDSNRdetDBScale] %s has not enough data samples' % currDev
                        validhist = dfCurrValidDev.edSNRdB.values
                        validhistFiltered = validhist
                        invalidhist = dfCurrInvalidDev.edSNRdB.values

                        dfPerformanceResult.loc[currDev].validPassCount = \
                            validhistFiltered.size
                        dfPerformanceResult.loc[currDev].validTotalCount = \
                            validhist.size
                        if validhist.size == 0:
                            dfPerformanceResult.loc[currDev].validPassRate = 0
                        else:
                            dfPerformanceResult.loc[currDev].validPassRate = \
                                float(validhistFiltered.size) / float(validhist.size)
                        dfPerformanceResult.loc[currDev].invalidFilteredCount = 0
                        dfPerformanceResult.loc[currDev].invalidTotalCount = \
                            invalidhist.size
                        dfPerformanceResult.loc[currDev].invalidFilteredRate = 0

                        print 'size of validhist           = %d' % validhist.size
                        print 'size of validhistFiltered   = %d' % validhistFiltered.size
                        print ' - pass rate      = %.2f%%' % (
                            dfPerformanceResult.loc[currDev].validPassRate * 100.0)
                        print 'size of invalidhist         = %d' % invalidhist.size
                        print 'size of invalidhistFiltered = %d' % 0
                        print ' - filtering rate = %.2f%%' % (0.0 * 100.0)
                        continue

                    dist = getattr(scipy.stats, modelinglist_curr)
                    invalidStudentTParam = dist.fit(y)
                    pdf_fitted_invalid = dist.pdf(pdf_resol, *invalidStudentTParam[:-2], loc=invalidStudentTParam[-2], scale=invalidStudentTParam[-1])
                    posterior_pdf_invalid = pdf_fitted_invalid * invalidPrior * InvalidBayesCost


                    dfValidStudentTParam.loc[currDev]      = list(validStudentTParam)
                    dfInvalidStudentTParam.loc[currDev]    = list(invalidStudentTParam)

                    logPosteriorRatio = np.log(posterior_pdf_invalid / posterior_pdf_valid)
                    edPassRange       = pdf_resol[np.where(logPosteriorRatio >= 0.0 )]
                    edPassRange = edPassRange[edPassRange > -2.0]

                    if isEDSNRdetRulePlot:
                        pyplot.plot(pdf_resol,posterior_pdf_valid,label='valid',color='blue')
                        pyplot.plot(pdf_resol,posterior_pdf_invalid,label='invalid',color='red')
                        pyplot.legend(loc='upper right')
                        pyplot.xlabel('edSNRdB')
                        pyplot.title((currDev))
                        pyplot.xlim([xmindB,xmaxdB])


                    if edPassRange.size > 0:

                        # gamma 찾는 알고리즘 보완필요
                        gamma1 = min(edPassRange)
                        gamma2 = max(edPassRange)
                        print '[runDesignEDSNRdetDBScale] edPassRange= %s' % edPassRange

                        dfEDFailRangedB.loc[currDev].gamma1              = gamma1
                        dfEDFailRangedB.loc[currDev].gamma2              = gamma2
                    else:
                        dfEDFailRangedB.loc[currDev].gamma1              = -9999  # all pass
                        dfEDFailRangedB.loc[currDev].gamma2              = -9999  # all pass

                    print '[runDesignEDSNRdetDBScale] gamma1  = %s' % dfEDFailRangedB.loc[currDev].gamma1
                    print '[runDesignEDSNRdetDBScale] gamma2  = %s' % dfEDFailRangedB.loc[currDev].gamma2

                    if isEDSNRperformanceResult:
                        validhist = dfCurrValidDev.edSNRdB.values
                        validhistFiltered = \
                            validhist[(validhist < dfEDFailRangedB.loc[currDev].gamma1) |\
                                      (validhist > dfEDFailRangedB.loc[currDev].gamma2)]
                        invalidhist = dfCurrInvalidDev.edSNRdB.values
                        invalidhistFiltered = invalidhist[invalidhist > dfEDFailRangedB.loc[currDev].gamma1]
                        invalidhistFiltered = \
                            invalidhistFiltered[invalidhistFiltered < dfEDFailRangedB.loc[currDev].gamma2]

                        dfPerformanceResult.loc[currDev].validPassCount              = \
                            validhistFiltered.size
                        dfPerformanceResult.loc[currDev].validTotalCount              = \
                            validhist.size
                        dfPerformanceResult.loc[currDev].validPassRate              = \
                            float(validhistFiltered.size) / float(validhist.size)
                        dfPerformanceResult.loc[currDev].invalidFilteredCount              = \
                            invalidhistFiltered.size
                        dfPerformanceResult.loc[currDev].invalidTotalCount              = \
                            invalidhist.size
                        dfPerformanceResult.loc[currDev].invalidFilteredRate = \
                            float(invalidhistFiltered.size) / float(invalidhist.size)


                        print 'size of validhist           = %d' % validhist.size
                        print 'size of validhistFiltered   = %d' % validhistFiltered.size
                        print ' - pass rate      = %.2f%%' % (
                        float(validhistFiltered.size) / float(validhist.size) * 100.0)
                        print 'size of invalidhist         = %d' % invalidhist.size
                        print 'size of invalidhistFiltered = %d' % invalidhistFiltered.size
                        print ' - filtering rate = %.2f%%' % (
                            float(invalidhistFiltered.size) / float(invalidhist.size) * 100.0)
                else:
                    print 'The # of samples is too small to execute the modeling for ED SNR!'
                    validhist = dfCurrValidDev.edSNRdB.values
                    validhistFiltered = validhist
                    invalidhist = dfCurrInvalidDev.edSNRdB.values

                    dfPerformanceResult.loc[currDev].validPassCount = \
                        validhistFiltered.size
                    dfPerformanceResult.loc[currDev].validTotalCount = \
                        validhist.size
                    if validhist.size == 0:
                        dfPerformanceResult.loc[currDev].validPassRate = 0
                    else:
                        dfPerformanceResult.loc[currDev].validPassRate = \
                            float(validhistFiltered.size) / float(validhist.size)
                    dfPerformanceResult.loc[currDev].invalidFilteredCount = 0
                    dfPerformanceResult.loc[currDev].invalidTotalCount = \
                        invalidhist.size
                    dfPerformanceResult.loc[currDev].invalidFilteredRate = 0

                    print 'size of validhist           = %d' % validhist.size
                    print 'size of validhistFiltered   = %d' % validhistFiltered.size
                    print ' - pass rate      = %.2f%%' % (
                        dfPerformanceResult.loc[currDev].validPassRate * 100.0)
                    print 'size of invalidhist         = %d' % invalidhist.size
                    print 'size of invalidhistFiltered = %d' % 0
                    print ' - filtering rate = %.2f%%' % ( 0.0 * 100.0)

            dfEDSNRDetDesign = pd.concat([dfEDSNRDetDesign, dfValidStudentTParam, dfInvalidStudentTParam], axis=1)


            dfEDSNRDetDesign.to_csv(ANAfile_DIR + 'EDSNRdetDesign_ValidBayesCost' + str(ValidBayesCost) + '_'+modelingNameList_curr+'_TPDF_dBScale.csv', encoding='utf-8')
            dfEDFailRangedB.to_csv(ANAfile_DIR + 'EDSNRDet_EDFAILrangedB_ValidBayesCost' + str(ValidBayesCost) +  '_'+modelingNameList_curr+'_TPDF_dBscale.csv',encoding='utf-8')

            dfPerformanceResult = pd.concat([dfEDFailRangedB, dfPerformanceResult], axis=1)
            dfPerformanceResult.to_csv(ANAfile_DIR + 'EDSNRDet_EDPerformanceResult_ValidBayesCost' + str(ValidBayesCost) +  '_'+modelingNameList_curr+'_TPDF_dBscale.csv',encoding='utf-8')
            if isEDSNRdetRulePlot:
                hfig1.savefig(currFIGfile_DIR + analysisdate + '_edSNRdB_DetRule_ValidBayesCost' + str(ValidBayesCost) + '_'+modelingNameList_curr+'_TPDF_dBScale.png')

    else:
        print '# [runDesignEDSNRdetDBScale] No Invalid Beacon for %s' % currSdkType
