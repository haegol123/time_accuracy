#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: runAnalyzeFalseAlarmPattern.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------

import sys
from os import getcwd
from os import system
sys.path.insert(0, getcwd()+'/python_codes')

import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as matplot
import intro
import subprocess


# signalType = 'yapp'
# signalType = 'lottecinema'
# signalType = 'dalkomm'
signalType = 'speaker'


if signalType == 'yapp':
    REF_PHONENAME_LIST = ['g5', 'grandmax', 'note5']
    refdate = '20170407'
elif signalType == 'lottecinema':
    REF_PHONENAME_LIST = ['note5','note2','note3','s4','g3','grandmax']
    refdate = '20170406'
elif signalType == 'dalkomm':
    REF_PHONENAME_LIST = ['a5','g2','j5','j7','note3','noteedge','s3','s5','s7']
    # REF_PHONENAME_LIST = ['a5']
    refdate = '20170407'
elif signalType == 'speaker':
    REF_PHONENAME_LIST = ['s7edge']
    # REF_PHONENAME_LIST = ['a5']
    refdate = '20170407'

system ('clear')

isEDPattern  = True
isPCSpattern = True
isBeaconIDhist = True
isPlot = True


FIG_SAVE_DIR            = getcwd() + '/fig/falseAlarmData/'+ signalType
FIG_SAVE_DIR_DATE       = FIG_SAVE_DIR + '/'+ refdate
FIG_SCATTER_SAVE_DIR    = FIG_SAVE_DIR_DATE + '/scatter/'
FIG_HIST_SAVE_DIR       = FIG_SAVE_DIR_DATE + '/hist/'

subprocess.call('mkdir {}'.format(FIG_SAVE_DIR), shell=True)
subprocess.call('mkdir {}'.format(FIG_SAVE_DIR_DATE), shell=True)
subprocess.call('mkdir {}'.format(FIG_SCATTER_SAVE_DIR), shell=True)
subprocess.call('mkdir {}'.format(FIG_HIST_SAVE_DIR), shell=True)


intro.intro_FalseAlarmAnalysis()


print '# [runAnalyzeFalseAlarmPattern] Configuration'
print '# [runAnalyzeFalseAlarmPattern] isEDPattern = %s' % isEDPattern
print '# [runAnalyzeFalseAlarmPattern] isPCSpattern = %s' % isPCSpattern
print '# -------------------------------------------------------------'


### phone count histogram


# reading reference data  and plotting
for i in range(0,len(REF_PHONENAME_LIST)):
    currdate = datetime.date(int(refdate[0:4]),int(refdate[4:6]),int(refdate[6:8]))

    ref_devicename = REF_PHONENAME_LIST[i]

    ref_csvfilename_sigO = str(currdate) + '_CoreParamTuningDataFrame_V3.05_FrameType2_' + ref_devicename +'.csv'

    REF_DATAFRAME_SIGO_CSV_FILENAME = getcwd() + '/csvfiles/falseAlarmData/' +signalType +'/' + ref_csvfilename_sigO

    ref_dataframe_sigO = pd.read_csv(REF_DATAFRAME_SIGO_CSV_FILENAME)


    if isPlot:
        ## reference data
        # ED Ty dB
        ref_df_EDTy_sigO = ref_dataframe_sigO['ED_T(y)']
        # ED SNR dB
        ref_df_EDSNR_sigO = ref_dataframe_sigO['ED_SNRdB']
        # preambleJMAR
        ref_df_pCSJMAR_sigO       = ref_dataframe_sigO['preambleJMAR']

        ref_df_dataParRatio_sigO    = ref_dataframe_sigO['dataParRatio']

        ref_df_dataPar_sigO         = ref_dataframe_sigO['dataPar']


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
        
        if isEDPattern:
            fig2 = matplot.figure(i+1000,figsize=(10,10))
            matplot.subplot(2,1,1)
            matplot.scatter(ref_df_EDTy_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('ED T(y) <dB>')
            matplot.title('Scatter plot '+ ref_devicename + ' ' + signalType)
            matplot.xlim([-110,-30])
            matplot.ylim([-20,50])
            # matplot.legend(['Rx - '+ signalType +' (FrameTypeZero) '])
            matplot.grid()

        if isPCSpattern:
            ax2 = matplot.subplot(2,1,2)
            matplot.scatter(ref_df_pCSJMAR_sigO,ref_df_EDSNR_sigO,color='b',marker='o')
            matplot.ylabel('ED SNR <dB>')
            matplot.xlabel('PreambleJCsMar')
            matplot.title('Scatter plot '+ ref_devicename + ' ' + signalType)
            matplot.xlim([0,50])
            matplot.ylim([-20,50])
            # matplot.legend(['Rx - LottenCinema (FrameTypeZero) '])
            matplot.grid()



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

        if isBeaconIDhist:
            beaconID = ref_dataframe_sigO[ref_dataframe_sigO['decodingResult'] > -1].decodingResult
            fig3 = matplot.figure(i+2000,figsize=(10,10))
            beaconID.hist(bins=[elem for elem in range(0,15)])
            matplot.ylabel('Count')
            matplot.xlabel('BeaconID')
            matplot.title('Histogram plot ' + ref_devicename + ' ' + signalType)
            matplot.xlim([0, 15])

        # fig1.savefig(FIG_HIST_SAVE_DIR +  'hist_'+ref_devicename+'.png')
        fig2.savefig(FIG_SCATTER_SAVE_DIR + 'scatter_FA_'+ref_devicename+'.png')
        fig3.savefig(FIG_HIST_SAVE_DIR + 'beaconID_hist_FA_'+ref_devicename+'.png')





