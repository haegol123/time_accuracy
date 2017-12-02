#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: common.py
# soundlly detect log format:
# https://github.com/soundlly/LogFormat/blob/master/log/detect_smarton.json
#
# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------

from os import getcwd


# file directory information for file import
RAW_CORELOG_DIR     = getcwd()  + '/rawCoreLog'
RAW_BEACONLOG_DIR   = getcwd()  + '/rawBeaconLog'
RAW_SCHEDULE_DIR    = getcwd()  + '/rawScheduleLog'
RAW_ACTIVE_DIR      = getcwd()  + '/rawActiveLog'
RAW_DETECT_DIR      = getcwd() +  '/rawDetectLog'
RAW_CUSTOM_DIR      = getcwd() +  '/rawCustomLog'
RAW_MONITORING_DIR     = getcwd() + '/rawMonitoringLog'

RAW_WAV_FILES_DIR      = getcwd() +  '/rawWavFiles'

# file directory information for file export
DAILY_DATAFRAME_BEACON_CSV_DIR     =   getcwd() +      '/csvfiles/dailyDataFrame/beacon'
DAILY_DATAFRAME_DETECT_CSV_DIR     =   getcwd() +      '/csvfiles/dailyDataFrame/detect'
DAILY_DATAFRAME_CUSTOM_CSV_DIR     =   getcwd() +      '/csvfiles/dailyDataFrame/custom'
DAILY_DATAFRAME_SCHEDULE_CSV_DIR     =   getcwd() +      '/csvfiles/dailyDataFrame/schedule'
DAILY_DATAFRAME_MONITORING_CSV_DIR     =   getcwd() +      '/csvfiles/dailyDataFrame/monitoring'

# DAILY_PERF_CSV_DIR          =   getcwd() +      '/csvfiles/performance/daily'
# DAILY_FA_REPORT_CSV_DIR     =   getcwd() +      '/csvfiles/falseAlarmReport/daily'
# WEEKLY_PERF_CSV_DIR         =   getcwd() +      '/csvfiles/performance/weekly'
# WEEKLY_FA_REPORT_CSV_DIR    =   getcwd() +      '/csvfiles/falseAlarmReport/weekly'

LOGFILE_DIR = '/tmp/exelog_runImportLog'

####====================================================================================================================
# The original label from core logs in Bitsound SDK
# which is used in genDataFrame.py
# the label name should be corresponding to the core log label name in Bitsound SDK
CUMSTOMLOG_LABEL   = ['appName', 'appKey' ,'deviceTime', 'phoneModel']
CORELOG_NAME = 'coreLogs'
CORELOG_HEAD_LABEL      = ['deviceIndex','timestamp']
CORELOG_ED_LABEL   = ['SNRdB','isEnergy','stat']
CORELOG_DATA_LABEL = ['coreVersion',       'dataJCsParGeqCounter','dataJCsParRatioGeqCounter',\
                        'decodingResult',    'frameType',           'isDataCsPass',             \
                        'isPreambleCsPass',  'preambleJCsMar',      'ricianKFactor_dB',\
                        'spreadingTime_sec']

ALL_TYPE_OF_PHONES = '*'
ED_NAME = 'ed'
ED_ISENERGY_NAME = CORELOG_ED_LABEL[1]
CORE_DATA_NAME = 'data'
CORE_APPKEY_NAME       = CUMSTOMLOG_LABEL[1]
CORE_PHONEMODEL_NAME   = CUMSTOMLOG_LABEL[3]
CORELOG_DATA_REMOVED_LABEL = ['preambleRakePeakNum','rakeOffsets','chAttenGain']

##----------------------------------------------------
# The original label from beacon logs in Bitsound SDK
BEACONLOG_NAME      = 'beaconLogs'
BEACONLOG_LABEL         = ['appName', 'appKey' , 'beacon','sequence', 'tryCount','deviceTime','phoneModel','netOper']
BEACON_BEACON_NAME  = BEACONLOG_LABEL[2]
BEACON_SEQ_NAME     = BEACONLOG_LABEL[3]
BEACON_TRYCNT_NAME  = BEACONLOG_LABEL[4]
BEACON_IS_VALID_BEACONNAME = ['isValidBeaconID']



##----------------------------------------------------
# The original label from beacon logs in Bitsound SDK
DETECTLOG_NAME      = 'detectLogs'
CORE_NAME           = 'core'
DATA_NAME           = 'data' # Temporarily used for json sub hierarchy of detect log, Sep 2017 (SWKA)

#--------------------------------------------
# format until the end of 20170712 log
# DETECTLOG_LABEL         = ['contentsName', 'appKey' , 'beacon','sequence','retry','deviceTime','phoneModel','sdkType','sdkVer']
# DETECT_BEACON_NAME  = DETECTLOG_LABEL[2]
# DETECT_SEQ_NAME     = DETECTLOG_LABEL[3]

#------------------------------------------------
# 170717 update by jwkang
# detect log since 20170713
# soundlly detect log format:
# https://github.com/soundlly/LogFormat/blob/master/log/detect_smarton.json
DETECTLOG_LABEL         = [ 'appKey' , 'beacon','retry','deviceTime','phoneModel','sdkType','sdkVer']
DETECT_BEACON_NAME  = DETECTLOG_LABEL[1]


DETECT_IS_VALID_BEACONNAME = ['isValidBeaconID']

##----------------------------------------------------
# The original label from custom logs in User test app
CUSTOMLOG_CORE_LABEL = ['appKey','deviceTime','phoneModel','sdkType','sdkVer']
CORE_CUSTOM_LOG_PARSE_NAME    = 'customLogs'
CORE_DATA_PARSE_NAME = 'coreData'

# CUSTOMLOG_CORE_LABEL = ['CORE_DETECTION_START',\
# 'CORE_DETECTION_ED_FAIL',\
# 'CORE_DETECTION_SUCCESS',\ # BEACON 수신 (값>) => 음파 수집 AWS S3 저장
# 'CORE_DETECTION_RESULT_ZERO',\ # BEACON 0 => 음파 수집 후 AWS S3 저장
# 'CORE_DETECTION_RESULT_NONE',\
# 'CORE_DETECTION_RESULT_AMBIGUOUS',\
# 'CORE_DETECTION_RESULT_CRCERROR',\
# 'CORE_DETECTION_RESULT_FATALERROR',\
# 'CORE_DETECTION_RESULT_RECORDFAIL',\
# 'CORE_DETECTION_RESULT_CSFAIL',\
# 'CORE_DETECTION_RESULT_MIC_ERROR',\ # => SDK정의 : 마이크 에러
# 'CORE_DETECTION_RESULT_UNKNOWN_ERROR']

#-----------------------------------------------------
#schedule 파일을 위한 라벨
SCHEDULELOG_LABEL=['schedule'] #제일 겉에 있는 칼럼
SCHEDULE_LOG_PARSE_BEACON = ['beacon']   #나중에 뽑아낼 데이터 칼럼
SCHEDULE_LOG_PARSE_TIME=['time']
SCHEDULE_LOG_PARSE_NAME='schedule'

#측정 데이터를 위한 라벨
MONITORINGLOG_LABEL         = [ 'appKey', 'beacon','serverTime','phoneModel','sdkType']

####==================================================================================================================
# The label used in the Data analysis Framework in python
# which is used in logAnalyzer.py
# label for dataframe structure
CUMSTOMLOG_LABEL_FRAME   = ['appName', 'appKey'  ,'deviceTime', 'phoneModel']
CORELOG_HEAD_LABEL_FRAME      = ['deviceIndex','CoreTimestamp']
CORELOG_ED_LABEL_FRAME   = ['SNRdB','isEnergy','stat']
CORELOG_DATA_LABEL_FRAME = ['coreVersion',       'dataJCsParGeqCounter','dataJCsParRatioGeqCounter',\
                            'decodingResult',    'FrameType',           'isDataCsPass',             \
                            'isPreambleCsPass',  'preambleJCsMar',      'ricianKFactor_dB',\
                            'spreadingTime_sec', 'isCRCPass','beaconID','isValidBeaconID']
FRAME_LABELS = CUMSTOMLOG_LABEL_FRAME + CORELOG_HEAD_LABEL_FRAME + CORELOG_ED_LABEL_FRAME + CORELOG_DATA_LABEL_FRAME

# ED name
EDSNRNAME  = CORELOG_ED_LABEL_FRAME[0]
EDPASSNAME = CORELOG_ED_LABEL_FRAME[1]
EDTyDBNAME = CORELOG_ED_LABEL_FRAME[2]

# data label name
DCSPARGEQCntNAME        = CORELOG_DATA_LABEL_FRAME[1]
DCSPARRATIOGEQCntNAME   = CORELOG_DATA_LABEL_FRAME[2]
DCSPASSNAME             = CORELOG_DATA_LABEL_FRAME[5]
PCSPASSNAME             = CORELOG_DATA_LABEL_FRAME[6]
PCSJMARNAME             = CORELOG_DATA_LABEL_FRAME[7]
RICIANKFACTORNAME       = CORELOG_DATA_LABEL_FRAME[8]
SPREADINGTIMENAME       = CORELOG_DATA_LABEL_FRAME[9]
CRCPASSNAME             = CORELOG_DATA_LABEL_FRAME[10]

class Common(object):
    def __init__(self):
        self.isInit = True

    def getDailyDataFrameCsvDir(self, logtype):
        if logtype == 'beacon':
            return DAILY_DATAFRAME_BEACON_CSV_DIR
        elif logtype == 'detect':
            return DAILY_DATAFRAME_DETECT_CSV_DIR
        elif logtype == 'custom':
            return DAILY_DATAFRAME_CUSTOM_CSV_DIR
        elif logtype == 'schedule':
            return DAILY_DATAFRAME_SCHEDULE_CSV_DIR
        elif logtype == 'monitoring':
            return DAILY_DATAFRAME_MONITORING_CSV_DIR
        else:
            print '# [Common] The logtype \"%s\" is not valid!' % logtype