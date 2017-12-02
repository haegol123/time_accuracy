#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runAnalyzeLogEDPattern.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------

import sys
from os import getcwd
from os import system
sys.path.insert(0, getcwd()+'/python_codes')

from datetime import date
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as matplot
import intro


LOG_PHONENAME_LIST = ['SM-N916','SM-N920','SM-G920','SM-G930','LG-F700','LG-F500']
REF_PHONENAME_LIST = ['note4','note5','s6','s7','g5','g4']

# LOG_PHONENAME_LIST = ['SM-N920']
# REF_PHONENAME_LIST = ['note5']



logdatelist = ['20170317',\
               '20170318',\
               '20170319',\
               '20170320',\
               '20170325']
refdate='20170329'

system ('clear')


isAnalyzeEDPASSLOG  = False
isAnalyzePCSPASSLOG = False
isAnalyzeCRCPASSLOG = True
isBeaconIDhist = True
isPlot = True


FIG_SAVE_DIR_DATE       = getcwd() + '/fig/corelogData/' + refdate
FIG_SCATTER_SAVE_DIR    = FIG_SAVE_DIR_DATE + '/scatter/'
FIG_HIST_SAVE_DIR       = FIG_SAVE_DIR_DATE + '/hist/'

intro.intro_EDAnalysis()


print '# [runAnalyzeEDPattern] Configuration'
print '# [runAnalyzeEDPattern] isAnalyzeEDPASSLOG = %s' % isAnalyzeEDPASSLOG
print '# [runAnalyzeEDPattern] isAnalyzePCSPASSLOG = %s' % isAnalyzePCSPASSLOG
print '# [runAnalyzeEDPattern] isAnalyzeCRCPASSLOG = %s' % isAnalyzeCRCPASSLOG
print '# -------------------------------------------------------------'

# log data processing
#1) collecting all netOpt data to one dataframe
log_dataframe_valid      =   DataFrame()
log_dataframe_invalid    =   DataFrame()
log_dataframe_edpass     =   DataFrame()
log_dataframe_pcspass     =   DataFrame()

for i in range(0,len(logdatelist)):
    logdate = logdatelist[i]

    # EDPASS log
    if isAnalyzeEDPASSLOG:
        log_csvfilename = str(logdate) + '_coreLog_DailyDataFrameEDPASS.csv'
        LOG_DATAFRAME_EDPASS_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_csvfilename
        currdataframe_edpass = pd.read_csv(LOG_DATAFRAME_EDPASS_CSV_FILENAME)
        print '# [runAnalyzeEDPattern] EDPASS CSV reading done! @ %s' % LOG_DATAFRAME_EDPASS_CSV_FILENAME

        log_dataframe_edpass   = pd.concat([log_dataframe_edpass,   currdataframe_edpass],   ignore_index=True)
        print '# [runAnalyzeEDPattern] EDPASS logsize is %s' % currdataframe_edpass.index.size
        print '# --------------------------------------------------------------------------------------------#'

    # PCSPASS log
    if isAnalyzePCSPASSLOG:
        log_csvfilename = str(logdate) + '_coreLog_DailyDataFramePCSPASS.csv'
        LOG_DATAFRAME_PCSPASS_CSV_FILENAME = getcwd() + '/csvfiles/dailyDataFrame/' + log_csvfilename
        currdataframe_pcspass = pd.read_csv(LOG_DATAFRAME_PCSPASS_CSV_FILENAME)
        print '# [runAnalyzeEDPattern] PCSPASS CSV reading done! @ %s' % LOG_DATAFRAME_PCSPASS_CSV_FILENAME

        log_dataframe_pcspass   = pd.concat([log_dataframe_pcspass,   currdataframe_pcspass],   ignore_index=True)
        print '# [runAnalyzeEDPattern] PCSPASS logsize is %s' % currdataframe_pcspass.index.size
        print '# --------------------------------------------------------------------------------------------#'


    # CRCPASS log
    if isAnalyzeCRCPASSLOG:
        log_csvfilename                     = str(logdate) + '_coreLog_DailyDataFrameCRCPASS.csv'
        LOG_DATAFRAME_CRCPASS_CSV_FILENAME  = getcwd() + '/csvfiles/dailyDataFrame/' + log_csvfilename
        currdataframe                       = pd.read_csv(LOG_DATAFRAME_CRCPASS_CSV_FILENAME)
        print '# [runAnalyzeEDPattern] CRCPASS CSV reading done! @ %s' % LOG_DATAFRAME_CRCPASS_CSV_FILENAME

        currdataframe_crcpass_valid     = currdataframe[currdataframe['isValidBeaconID'] ==  True]
        currdataframe_crcpass_invalid   = currdataframe[currdataframe['isValidBeaconID'] == False]
        log_dataframe_valid     = pd.concat([log_dataframe_valid,   currdataframe_crcpass_valid],   ignore_index=True)
        log_dataframe_invalid   = pd.concat([log_dataframe_invalid, currdataframe_crcpass_invalid], ignore_index=True)
        print '# [runAnalyzeEDPattern] CRCPASS logsize with valid beacon is %s' % currdataframe_crcpass_valid.index.size
        print '# [runAnalyzeEDPattern] CRCPASS logsize with invalid beacon is %s' % currdataframe_crcpass_invalid.index.size
        print '# [runAnalyzeEDPattern] Rate of invalid beacon over total CRCPASS = %1.4f' % (float(currdataframe_crcpass_invalid.index.size)/float(currdataframe.index.size) )
        print '# --------------------------------------------------------------------------------------------#'
        currdataframe = None


if isAnalyzeCRCPASSLOG:
    print '# [runAnalyzeEDPattern] Total logsize dataframe with valid beacon is %s' % log_dataframe_valid.index.size
    print '# [runAnalyzeEDPattern] Total logsize dataframe with invalid beacon is %s' % log_dataframe_invalid.index.size
    print '# --------------------------------------------------------------------------------------------#'

### phone count histogram
# phoneModelFrame =  log_dataframe.phoneModel
# phoneModelFrame.value_counts().plot(kind='bar')

# reading reference data  and plotting
for i in range(0,len(LOG_PHONENAME_LIST)):
    currdate = date(int(refdate[0:4]),int(refdate[4:6]),int(refdate[6:8]))

    ref_devicename = REF_PHONENAME_LIST[i]
    log_devicename = LOG_PHONENAME_LIST[i]

    ref_csvfilename_sigO = str(currdate) + '_CoreParamTuningDataFrame_V3.05_FrameType2_' + ref_devicename +'_SigO.csv'
    ref_csvfilename_sigX = str(currdate) + '_CoreParamTuningDataFrame_V3.05_FrameType2_' + ref_devicename +'_SigX.csv'

    REF_DATAFRAME_SIGO_CSV_FILENAME = getcwd() + '/csvfiles/refdata/' + ref_csvfilename_sigO
    REF_DATAFRAME_SIGX_CSV_FILENAME = getcwd() + '/csvfiles/refdata/' + ref_csvfilename_sigX

    ref_dataframe_sigO = pd.read_csv(REF_DATAFRAME_SIGO_CSV_FILENAME)
    ref_dataframe_sigX = pd.read_csv(REF_DATAFRAME_SIGX_CSV_FILENAME)

    if isAnalyzeCRCPASSLOG:
        # crcpass valid log
        phoneNameFrame = DataFrame(data = [elem.find(log_devicename) > -1 for elem in list(log_dataframe_valid['phoneModel'].values)])
        phoneNameFrame_index = phoneNameFrame[phoneNameFrame[0] == True].index
        log_dataframe_valid_device      = log_dataframe_valid.loc[phoneNameFrame_index]

        # crcpass invalid log
        phoneNameFrame                          = DataFrame(data = [elem.find(log_devicename) > -1 for elem in list(log_dataframe_invalid['phoneModel'].values)])
        phoneNameFrame_index                    = phoneNameFrame[phoneNameFrame[0] == True].index
        log_dataframe_invalid_device            = log_dataframe_invalid.loc[phoneNameFrame_index]
        log_dataframe_invalid_zero_device       = log_dataframe_invalid_device[log_dataframe_invalid_device['beaconID'] == 0]
        log_dataframe_invalid_nonzero_device    = log_dataframe_invalid_device[log_dataframe_invalid_device['beaconID'] > 0 ]
        print '# [runAnalyzeEDPattern] # of Invalid zero beacon of %s = %s' % (ref_devicename,log_dataframe_invalid_zero_device.index.size)
        print '# [runAnalyzeEDPattern] # of Invalid Nonzero beacon of %s = %s' % (ref_devicename,log_dataframe_invalid_nonzero_device.index.size)
        print '# [runAnalyzeEDPattern[ Rate of zero beacon over total invalid beacon = %1.4f' % (float(log_dataframe_invalid_zero_device.index.size)/float(log_dataframe_invalid_device.index.size))

    if isAnalyzePCSPASSLOG:
        # pcspass log
        phoneNameFrame                          = DataFrame(data = [elem.find(log_devicename) > -1 for elem in list(log_dataframe_pcspass['phoneModel'].values)])
        phoneNameFrame_index                    = phoneNameFrame[phoneNameFrame[0] == True].index
        log_dataframe_pcspass_device             = log_dataframe_pcspass.loc[phoneNameFrame_index]


    if isAnalyzeEDPASSLOG:
        # edpass log
        phoneNameFrame                          = DataFrame(data = [elem.find(log_devicename) > -1 for elem in list(log_dataframe_edpass['phoneModel'].values)])
        phoneNameFrame_index                    = phoneNameFrame[phoneNameFrame[0] == True].index
        log_dataframe_edpass_device             = log_dataframe_edpass.loc[phoneNameFrame_index]
        if isAnalyzePCSPASSLOG == False:
            log_dataframe_pcspass_device            = log_dataframe_edpass_device[log_dataframe_edpass_device['isPreambleCsPass'] == True]
        log_dataframe_pcsfail_device            = log_dataframe_edpass_device[log_dataframe_edpass_device['isPreambleCsPass'] == False]


    if isPlot:
        ## reference data
        # ED Ty dB
        ref_df_EDTy_sigO = ref_dataframe_sigO['ED_T(y)']
        ref_df_EDTy_sigX = ref_dataframe_sigX['ED_T(y)']
        # ED SNR dB
        ref_df_EDSNR_sigO = ref_dataframe_sigO['ED_SNRdB']
        ref_df_EDSNR_sigX = ref_dataframe_sigX['ED_SNRdB']
        # preambleJMAR
        ref_df_pCSJMAR_sigO       = ref_dataframe_sigO['preambleJMAR']
        ref_df_pCSJMAR_sigX       = ref_dataframe_sigX['preambleJMAR']

        ref_df_dataParRatio_sigO    = ref_dataframe_sigO['dataParRatio']
        ref_df_dataParRatio_sigX    = ref_dataframe_sigX['dataParRatio']

        ref_df_dataPar_sigO         = ref_dataframe_sigO['dataPar']
        ref_df_dataPar_sigX         = ref_dataframe_sigX['dataPar']

        if isAnalyzeCRCPASSLOG:
            # ED Ty dB
            log_valid_EDTy_df           = log_dataframe_valid_device['stat']
            log_invalid_EDTy_df         = log_dataframe_invalid_device['stat']
            log_invalid_zero_EDTy_df    = log_dataframe_invalid_zero_device['stat']
            log_invalid_nonzero_EDTy_df = log_dataframe_invalid_nonzero_device['stat']
            # ED SNR dB
            log_valid_EDSNR_df              = log_dataframe_valid_device['SNRdB']
            log_invalid_EDSNR_df            = log_dataframe_invalid_device['SNRdB']
            log_invalid_zero_EDSNR_df       = log_dataframe_invalid_zero_device['SNRdB']
            log_invalid_nonzero_EDSNR_df    = log_dataframe_invalid_nonzero_device['SNRdB']
            # preambleJMAR
            log_valid_pCSJMAR_df            = log_dataframe_valid_device['preambleJCsMar']
            log_invalid_zero_pCSJMAR_df     = log_dataframe_invalid_zero_device['preambleJCsMar']
            log_invalid_nonzero_pCSJMAR_df  = log_dataframe_invalid_nonzero_device['preambleJCsMar']

            log_invalid_zero_dataParRatio   = log_dataframe_invalid_zero_device['dataJCsParRatioGeqCounter']
            log_invalid_zero_dataPar        = log_dataframe_invalid_zero_device['dataJCsParGeqCounter']

            log_invalid_nonzero_dataParRatio   = log_dataframe_invalid_nonzero_device['dataJCsParRatioGeqCounter']
            log_invalid_nonzero_dataPar        = log_dataframe_invalid_nonzero_device['dataJCsParGeqCounter']

        if isAnalyzePCSPASSLOG:
            log_pcspass_EDSNR_df = log_dataframe_pcspass_device['SNRdB']
            log_pcspass_pCSJMAR_df = log_dataframe_pcspass_device['preambleJCsMar']

        if isAnalyzeEDPASSLOG:
            if isAnalyzePCSPASSLOG == False:
                log_pcspass_EDSNR_df    = log_dataframe_pcspass_device['SNRdB']
                log_pcspass_pCSJMAR_df  = log_dataframe_pcspass_device['preambleJCsMar']

            log_pcsfail_EDSNR_df    =   log_dataframe_pcsfail_device['SNRdB']
            log_pcsfail_pCSJMAR_df  = log_dataframe_pcsfail_device['preambleJCsMar']


        ## plotting figure
        # fig1 = matplot.figure(i)
        # matplot.subplot(2,1,1)
        # ref_df_EDTy_sigO.plot(title='PMF of ED_T(y)dB given CRCPASS '+ref_devicename,\
        #                                 kind='hist',bins=30, weights=np.ones_like(ref_df_EDTy_sigO*100.0)/len(ref_df_EDTy_sigO))
        # ax1 = ref_df_EDTy_sigX.plot(    kind='hist',bins=30, weights=np.ones_like(ref_df_EDTy_sigX*100.0)/len(ref_df_EDTy_sigX))
        # log_valid_EDTy_df.plot(kind='hist',bins=30, weights=np.ones_like(log_valid_EDTy_df*100.0)/len(log_valid_EDTy_df)).legend(['ref sigO','ref sigX','log CRCPASS + valid Beacon'])
        # # ax.set_xlabel('ED_T(y) <dB>')
        # ax1.set_ylabel('Probability Mass')
        #
        # matplot.subplot(2,1,2)
        # ref_df_EDSNR_sigO.plot(title='PMF of ED_SNR dB given CRCPASS '+ref_devicename,\
        #                                       kind='hist', bins=30, weights=np.ones_like(ref_df_EDSNR_sigO * 100.0) / len(ref_df_EDSNR_sigO))
        # ax1 = ref_df_EDSNR_sigX.plot(kind='hist', bins=30, weights=np.ones_like(ref_df_EDSNR_sigX * 100.0) / len(ref_df_EDSNR_sigX))
        #
        # log_valid_EDSNR_df.plot(kind='hist', bins=30, weights=np.ones_like(log_valid_EDSNR_df * 100.0) / len(log_valid_EDSNR_df)).legend(['ref sigO','ref sigX','log CRCPASS + valid Beacon'])
        # # ax.set_xlabel('ED_SNR <dB>')
        # ax1.set_ylabel('Probability Mass')
        if isAnalyzeCRCPASSLOG:
            fig2 = matplot.figure(i+1000,figsize=(20,20))
            matplot.subplot(3,2,1)
            matplot.scatter(ref_df_EDTy_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.scatter(ref_df_EDTy_sigX,ref_df_EDSNR_sigX,color='g',marker='o')
            matplot.scatter(log_valid_EDTy_df,log_valid_EDSNR_df,color='r',marker='x')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('ED T(y) <dB>')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([-110,-30])
            matplot.ylim([-20,50])
            matplot.legend(['ref sigO','ref sigX','log CRCPASS + valid Beacon'])

            matplot.subplot(3,2,2)
            matplot.scatter(log_invalid_nonzero_EDTy_df,log_invalid_nonzero_EDSNR_df,color='g',marker='o')
            matplot.scatter(log_invalid_zero_EDTy_df,log_invalid_zero_EDSNR_df,color='b',marker='o')
            matplot.scatter(log_valid_EDTy_df,log_valid_EDSNR_df,color='r',marker='x')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('ED T(y) <dB>')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([-110,-30])
            matplot.ylim([-20,50])
            matplot.legend(['log CRCPASS + InValid Beacon NonZero','log CRCPASS + InValid Beacon Zero','log CRCPASS + Valid Beacon'])


            ax2 = matplot.subplot(3,2,3)
            matplot.scatter(ref_df_pCSJMAR_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.scatter(ref_df_pCSJMAR_sigX,ref_df_EDSNR_sigX,color='g',marker='o')
            matplot.scatter(log_invalid_zero_pCSJMAR_df,log_invalid_zero_EDSNR_df,color='r',marker='x')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('PreambleJCsMar')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([0,50])
            matplot.ylim([-20,50])
            matplot.legend(['ref sigO','ref sigX','log CRCPASS + Invalid Zero'])

            matplot.subplot(3,2,4)
            matplot.scatter(ref_df_pCSJMAR_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.scatter(ref_df_pCSJMAR_sigX,ref_df_EDSNR_sigX,color='g',marker='o')
            matplot.scatter(log_invalid_nonzero_pCSJMAR_df,log_invalid_nonzero_EDSNR_df,color='r',marker='x')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('PreambleJCsMar')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([0,50])
            matplot.ylim([-20,50])
            matplot.legend(['ref sigO','ref sigX','log CRCPASS + Invalid NonZero'])

            matplot.subplot(3,2,5)
            matplot.scatter(ref_df_pCSJMAR_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.scatter(ref_df_pCSJMAR_sigX,ref_df_EDSNR_sigX,color='g',marker='o')
            matplot.scatter(log_valid_pCSJMAR_df,log_valid_EDSNR_df,color='r',marker='x')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('PreambleJCsMar')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([0,50])
            matplot.ylim([-20,50])
            matplot.legend(['ref sigO','ref sigX','log CRCPASS + Valid'])




        if isAnalyzeEDPASSLOG:
            matplot.subplot(3,2,6)
            matplot.scatter(log_pcspass_pCSJMAR_df,log_pcspass_EDSNR_df,color='b',marker='o')
            matplot.scatter(log_pcsfail_pCSJMAR_df,log_pcsfail_EDSNR_df,color='g',marker='o')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('PreambleJCsMar')
            matplot.title('Scatter plot '+ ref_devicename)
            matplot.xlim([0,50])
            matplot.ylim([-20,50])
            matplot.legend(['log PCSPASS','log PCSFAIL'])

        # if isAnalyzeCRCPASSLOG:
            # fig3 = matplot.figure(i+100,figsize=(15,10))
            # matplot.subplot(2,2,1)
            # matplot.hist2d(ref_df_dataPar_sigO,ref_df_dataParRatio_sigO,bins=10, normed=True)
            # matplot.ylabel('dataPar')
            # matplot.xlabel('dataParRatio')
            # matplot.legend(['ref sigO'])
            #
            # matplot.subplot(2,2,2)
            # matplot.hist2d(ref_df_dataPar_sigX,ref_df_dataParRatio_sigX,)
            # matplot.ylabel('dataPar')
            # matplot.xlabel('dataParRatio')
            # matplot.legend(['ref sigX'])
            #
            #
            # matplot.subplot(2,2,3)
            # matplot.hist2d(log_invalid_zero_dataPar,log_invalid_zero_dataParRatio)
            # matplot.ylabel('dataPar')
            # matplot.xlabel('dataParRatio')
            # matplot.legend(['invalid zero'])
            #
            #
            # matplot.subplot(2,2,4)
            # matplot.hist2d(log_invalid_nonzero_dataPar,log_invalid_nonzero_dataParRatio)
            # matplot.ylabel('dataPar')
            # matplot.xlabel('dataParRatio')
            # matplot.legend(['invalid nonzero'])
        if isBeaconIDhist:
            beaconID_nonzero = log_dataframe_invalid_nonzero_device[log_dataframe_invalid_nonzero_device['decodingResult'] > -1].decodingResult
            beaconID_zero = log_dataframe_invalid_zero_device[log_dataframe_invalid_zero_device['decodingResult'] > -1].decodingResult

            fig3 = matplot.figure(i+2000,figsize=(10,10))
            beaconID_nonzero.hist(bins=[elem for elem in range(0,15)],color='g')
            beaconID_zero.hist(width=1,color='b')
            matplot.ylabel('Count')
            matplot.xlabel('BeaconID')
            matplot.title('Histogram plot ' + ref_devicename )
            matplot.xlim([0, 15])

        # fig1.savefig(FIG_HIST_SAVE_DIR +  'hist_'+ref_devicename+'.png')
        fig2.savefig(FIG_SCATTER_SAVE_DIR + 'scatter_LOG_'+ref_devicename+'.png')
        fig3.savefig(FIG_HIST_SAVE_DIR + 'beaconID_hist_LOG_'+ref_devicename+'.png')

        # fig3.savefig(FIG_SCATTER_SAVE_DIR + 'scatter_dataCS_'+ref_devicename+'.png')




