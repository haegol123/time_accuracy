#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runDesignEDSNRdet.py.py
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


# logdatelist = ['20170715']
logdatelist = ['20170701',\
               '20170702',\
               '20170703',\
               '20170704',\
               # '20170707',\
               # '20170708',\
               # '20170709',\
               # '20170714',\
               # '20170715',\
               # '20170716',\
               # '20170717'
               ]
# sdkTypeList  = [ "smarton","receiver"]
sdkTypeList  = [ "smarton"]

system('clear')

isPerDevAnalysis = True


ValidBayesCost   = 0.3
InvalidBayesCost = 1.0 - ValidBayesCost

analysisdate = str(datetime.date.today())
analysisdate = analysisdate[0:4] + analysisdate[5:7] + analysisdate[8:10]

CSVfile_DIR = getcwd() + '/csvfiles/dailyDataFrame/detect/'
ANAfile_DIR = getcwd() + '/csvfiles/analysisResult/' + analysisdate + '/'

dist_names = ['norm','laplace','t']


subprocess.call('mkdir ' + CSVfile_DIR, shell=True)
subprocess.call('mkdir ' + ANAfile_DIR, shell=True)

intro.intro_DesignEDSNRdet()


print '# [runAnalysisDetectLog] Configration'
print '# [runAnalysisDetectLog] isPerDevAnalysis = %s' % isPerDevAnalysis


dfEntire        = DataFrame()
dfValidBeacon  = DataFrame()
dfInValidBeacon = DataFrame()


for i in range(0, len(logdatelist)):
    logdate = logdatelist[i]

    csvfilename = CSVfile_DIR + logdate + '_detectLog_DailyDataFrame.csv'

    print '# [runAnalysisDetectLog] Loading data from %s' % csvfilename

    curr_dataframe = pd.read_csv(csvfilename)

    if not(curr_dataframe.empty):
        dfEntire = pd.concat([dfEntire, curr_dataframe],ignore_index=True)
        print '# [runAnalysisDetectLog] beacon count of %s = %s' % (logdate, curr_dataframe.phoneModel.size)

print '# [runAnalysisDetectLog] csv loading done!'
dfEntire = dfEntire.reindex()


dfInValidBeacon = dfEntire[ dfEntire['isValidBeaconID'] == False]
dfValidBeacon   = dfEntire[ dfEntire['isValidBeaconID'] == True ]

dfInValidBeacon = dfInValidBeacon.reindex()
dfValidBeacon   = dfValidBeacon.reindex()

print '# -------------------------------------------------------------------------------------- '
print '# [runAnalysisDetectLog] log collecting period = %s' % logdatelist
print '# [runAnalysisDetectLog] Total beacon count = %s' % dfEntire.phoneModel.size
print '# [runAnalysisDetectLog] Total Invalid count = %s' % dfInValidBeacon.phoneModel.size

for k in range(0,len(sdkTypeList)):
    # classification of receiver and smarton data
    currSdkType = sdkTypeList[k]
    resolution = 10000
    xmin = 0
    xmax = resolution
    pdf_resol = np.linspace(xmin, xmax, xmax)
    minSampleSize = 50

    checkPhoneList = suppdevlist.ANDROID

    dfEntire_curr        = dfEntire         [dfEntire.sdkType.str.contains(currSdkType)]
    dfValidBeacon_curr   = dfValidBeacon    [dfValidBeacon.sdkType.str.contains(currSdkType)]
    dfInValidBeacon_curr = dfInValidBeacon  [dfInValidBeacon.sdkType.str.contains(currSdkType)]

    print '# -------------------------------------------------------------------------------------- '
    print '# [runAnalysisDetectLog] sdkType = %s' % currSdkType
    print '# [runAnalysisDetectLog] Total beacon count = %s' % dfEntire_curr.phoneModel.size
    print '# [runAnalysisDetectLog] Total Invalid count = %s' % dfInValidBeacon_curr.phoneModel.size
    print '# [runAnalysisDetectLog] ValidBayesCost = %s' % ValidBayesCost
    print '# [runAnalysisDetectLog] pdf resolution = %s' % resolution


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

            dfEDSNRDetDesign          =  pd.concat([beaconErrRateSupp, beaconRcvdRateSupp, beaconErrRateSupp/beaconRcvdRateSupp],axis=1)
            dfEDSNRDetDesign.columns   = ['Invalid Prior Rate','Valid Prior Rate','Invalid prior / Valid prior']
            dfValidBetaPrimeParam = DataFrame(index=suppdevlist.ANDROID, \
                                                  columns=['Valid BetaPrime a', 'Valid BetaPrime b',
                                                           'Valid BetaPrime loc', 'Valid BetaPrime scale'])

            dfInvalidBetaPrimeParam = DataFrame(index=suppdevlist.ANDROID, \
                                                    columns=['Invalid BetaPrime a', 'Invalid BetaPrime b',
                                                             'Invalid BetaPrime loc', 'Invalid BetaPrime scale'])

            dfEDFailRangedB           = DataFrame(index=suppdevlist.ANDROID,\
                                                    columns=['gamma1','gamma2'])
            for j in range(0,len(checkPhoneList)):
                currDev = checkPhoneList[j]
                dfCurrValidDev      = dfValidBeacon_curr  [dfValidBeacon_curr.phoneModel.str.contains(currDev)]
                dfCurrInvalidDev    = dfInValidBeacon_curr[dfInValidBeacon_curr.phoneModel.str.contains(currDev)]

                if dfCurrValidDev.size > minSampleSize and dfCurrInvalidDev.size > minSampleSize:
                    # likelihood pdf fitting for Valid

                    validPrior   = dfEDSNRDetDesign.loc[currDev]['Valid Prior Rate']
                    invalidPrior = dfEDSNRDetDesign.loc[currDev]['Invalid Prior Rate']


                    y                =  np.power(10,dfCurrValidDev.edSNRdB.values/10)
                    y                =  y[ y < xmax]
                    if y.size < minSampleSize:
                        continue

                    dist = getattr(scipy.stats, 'betaprime')

                    validBetaPrimeParam = dist.fit(y)
                    pdf_fitted_valid = dist.pdf(pdf_resol, *validBetaPrimeParam[:-2], loc=validBetaPrimeParam[-2], scale=validBetaPrimeParam[-1])
                    posterior_pdf_valid  = pdf_fitted_valid * validPrior * ValidBayesCost


                    # likelihood pdf fitting for invalid
                    y                =  np.power(10,dfCurrInvalidDev.edSNRdB.values/10)
                    y                =  y[ y < xmax]
                    if y.size < minSampleSize:
                        continue

                    dist = getattr(scipy.stats, 'betaprime')
                    invalidBetaPrimeParam = dist.fit(y)
                    pdf_fitted_invalid = dist.pdf(pdf_resol, *invalidBetaPrimeParam[:-2], loc=invalidBetaPrimeParam[-2], scale=invalidBetaPrimeParam[-1])
                    posterior_pdf_invalid = pdf_fitted_invalid * invalidPrior * InvalidBayesCost


                    dfValidBetaPrimeParam.loc[currDev]      = list(validBetaPrimeParam)
                    dfInvalidBetaPrimeParam.loc[currDev]    = list(invalidBetaPrimeParam)

                    logPosteriorRatio = np.log(posterior_pdf_invalid / posterior_pdf_valid)
                    edPassRange       = pdf_resol[np.where(logPosteriorRatio >= 0.0 )]
                    if edPassRange.size > 0:
                        gamma1 = min(edPassRange)
                        gamma2 = max(edPassRange)

                        if gamma1 == 0.0:
                            dfEDFailRangedB.loc[currDev].gamma1              = -999
                            if gamma2 == 0.0:
                                dfEDFailRangedB.loc[currDev].gamma2          = -999
                            else:
                                dfEDFailRangedB.loc[currDev].gamma2         = 10.0 * np.log10(gamma2)

                        else:
                            dfEDFailRangedB.loc[currDev].gamma1              = 10.0 * np.log10(gamma1)
                            dfEDFailRangedB.loc[currDev].gamma2              = 10.0 * np.log10(gamma2)
                    else:
                        dfEDFailRangedB.loc[currDev].gamma1              = -9999
                        dfEDFailRangedB.loc[currDev].gamma2              = -9999


            dfEDSNRDetDesign = pd.concat([dfEDSNRDetDesign, dfValidBetaPrimeParam, dfInvalidBetaPrimeParam], axis=1)

            dfEDSNRDetDesign.to_csv(ANAfile_DIR + 'EDSNRdetDesign_ValidBayesCost' + str(ValidBayesCost) + '.csv', encoding='utf-8')
            dfEDFailRangedB.to_csv(ANAfile_DIR + 'EDSNRDet_EDFAILrangedB_ValidBayesCost' + str(ValidBayesCost) + '.csv',encoding='utf-8')


    else:
        print '# [runAnalysisDetectLog] No Invalid Beacon for %s' % currSdkType


