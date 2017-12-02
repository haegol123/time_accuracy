#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: downlog.py
#
# This is python codes for Soundlly Logs downloading
# This is for Core performance measuring from Soundlly Logs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import subprocess
import common
import os
import sys
from datetime import datetime, date, time
import datetime


class LogDownloader (object):

    def __init__(self):
        self.mLogInfo = LogInfo()
        self.mFp = None
        self.mIsFileWrite = False

    def setLogInfo(self,currdate,logtype,servertype,appkey=str()):
        self.mLogInfo.configLog(currdate,logtype,servertype,appkey)

        if self.mIsFileWrite:
            self.mFp.write('# [LogInfo] LogDate = %s\n' % self.mLogInfo.mLogcurrdate)
            self.mFp.write('# [LogInfo] LogType = %s\n' % self.mLogInfo.mLogType)
            self.mFp.write('# [LogInfo] LogDirPath = %s\n' % self.mLogInfo.mLogDirPath)
            self.mFp.write('# [LogInfo] LogBucket = %s\n' % self.mLogInfo.mLogBucket)
            self.mFp.write('# ------------------------------------------------#\n')

    def downLogRecord(self):
        # target = 's3://{}/raw/{}'.format(self.mLogInfo.mLogBucket, str(self.mLogInfo.mLogDate)) # 20170712 로그까지 유호

        # raw_new / 2017 / mm /dd /detect /appkey
        yyyy = str(self.mLogInfo.mLogDate)[0:4]
        mm   = str(self.mLogInfo.mLogDate)[5:7]
        dd   = str(self.mLogInfo.mLogDate)[8:10]

        if self.mLogInfo.mLogAppKey.__len__() > 0:
            #측정 데이터 가져오기
            if self.mLogInfo.mLogType == 'monitoring':
                target = 's3://{}/raw_new{}/{}/{}/detect/{}'.format(self.mLogInfo.mLogBucket,yyyy,mm,dd,self.mLogInfo.mLogAppKey)

            elif self.mLogInfo.mLogType!='schedule':
                target = 's3://{}/raw_new/{}/{}/{}/{}/{}'.format(self.mLogInfo.mLogBucket, yyyy,mm,dd,self.mLogInfo.mLogType,self.mLogInfo.mLogAppKey) # 20170712 로그까지 유호

        #schedule file download YYYYMMDDHHMMSS format
        #elif len(str(self.mLogInfo.mLogDate)) > 10:
            #logHour=str(self.mLogInfo.mLogDate)[11:13]
            #logMinute=str(self.mLogInfo.mLogDate)[14:16]
            #logSecond=str(self.mLogInfo.mLogDate)[17:19]
            #target = 's3://bitsound.sdk.schedule/{}/schedule.{}.{}.{}.{}.{}.{}'.format(self.mLogInfo.mLogAppKey, yyyy, mm, dd, logHour, logMinute, logSecond)  # 상용서버 스케줄파일

         # # single schedule file format
         #    elif self.mLogInfo.mLogType=='schedule':
         #        target = 's3://{}/{}/schedule'.format(self.mLogInfo.mLogBucket,self.mLogInfo.mLogAppKey)  # 상용서버 앱키에 따른 스케줄 단일 파일(최신화파일)

            # another schedule format dev.bitsound.sdk.schedule / YYYY / MM / DD / schedule
            # https://s3-ap-northeast-1.amazonaws.com/dev.bitsound.sdk.schedule/schedule-accuracy/2017/10/27/schedule
            elif self.mLogInfo.mLogType=='schedule':
                target ='s3://{}/schedule-accuracy/{}/{}/{}/schedule'.format(self.mLogInfo.mLogBucket, yyyy, mm, dd)
            else:
                target = 's3://{}/raw_new/{}/{}/{}/{}/'.format(self.mLogInfo.mLogBucket, yyyy,mm,dd,self.mLogInfo.mLogType) # 20170712 로그까지 유호

        # Folder setup
        if not os.path.exists(self.mLogInfo.mLogDirPath):
            subprocess.check_call('mkdir {}'.format(self.mLogInfo.mLogDirPath), shell=True)
        location = self.mLogInfo.mLogDirPath + '/' + self.mLogInfo.mLogcurrdate

        try:
            subprocess.check_call('mkdir {}'.format(location), shell=True)
        except:
            print '# [LogDownloader] location = %s already exists!' % location
            if self.mIsFileWrite:
                self.mFp.write('# [LogDownloader] location = %s already exists!\n' % location)



        print '# [LogDownloader] target = %s' % target
        print '# [LogDownloader] location = %s' % location
        print '# [LogDownloader] sys.platform = %s' % sys.platform
        print '#----------------------------------------------------'

        if self.mIsFileWrite:
            self.mFp.write('# [LogDownloader] target = %s\n' % target)
            self.mFp.write('# [LogDownloader] location = %s\n' % location)
            self.mFp.write('# [LogDownloader] sys.platform = %s\n' % sys.platform)
            self.mFp.write('#----------------------------------------------------\n')

        #aws cli for schedule file from v1
        # schedule 파일을 s3 실사용서버로부터 다운로드 받는다
        # if self.mLogInfo.mLogType=='schedule' and sys.platform=='darwin':
            #tmpCLI='aws s3 cp {} {}'.format(target,location)
        # common 으로 갈 수가없음 넘겨줄 sys.platform 이 명확하지도 않음


        # make CLI string
        baseCLI = 'aws s3 cp {} {}'.format(target,location)
        optionCLI = '--recursive --exclude "*" --include "*{}*"{}'.format(self.mLogInfo.mLogType, self.mLogInfo.mLogGetFlag)
        callCLI = ''
        awsPath=''

        # mac OS
        if sys.platform == 'darwin':
            awsPath = ''

        # linux
        else:
            awsPath = '/usr/bin/'

        # schedule 파일이면 option 없음
        if self.mLogInfo.mLogType == 'schedule':
            callCLI = '{}{}'.format(awsPath, baseCLI)
        # 측정 데이터 가져오기
        elif self.mLogInfo.mLogType=='monitoring':
            callCLI = '{}{} --recursive --include "*"'.format(awsPath, baseCLI)

        # schedule 파일이 아니면 option 있음
        else:
            optionCLI = '--recursive --exclude "*" --include "*{}*"{}'.format(self.mLogInfo.mLogType, self.mLogInfo.mLogGetFlag)
            callCLI = '{}{} {}'.format(awsPath, baseCLI, optionCLI)
        # # CLI 호출 정하기
        # if self.mLogInfo.mLogType == 'schedule' and sys.platform == 'darwin':
        #     callCLI = baseCLI
        #
        # elif self.mLogInfo.mLogType != 'schedule' and sys.platform == 'darwin':
        #     callCLI = '{} {}'.format(baseCLI, optionCLI)
        #
        # elif self.mLogInfo.mLogType == 'schedule' and sys.platform != 'darwin':
        #     callCLI = '/usr/bin/{}'.format(baseCLI)
        #
        # # 다른 경우의 수 좀 더 추가 현재 리눅스
        # else:
        #     callCLI = '/usr/bin/{} {}'.format(baseCLI, optionCLI)

        # 정해진 CLI 호출
        subprocess.check_call('{}'.format(callCLI), shell=True)

        # if sys.platform == 'darwin':
            #subprocess.check_call(''.format(tmpCLI), shell=True)

            #subprocess.check_call('aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"{}'.format(target,location,self.mLogInfo.mLogType, self.mLogInfo.mLogGetFlag), shell=True)
            # subprocess.check_call('aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*15'), shell=True)
            # subprocess.check_call('aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*09'), shell=True)
            # subprocess.check_call('aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*18'), shell=True)


        #else:# sys.platform == 'linux2':
            #subprocess.check_call('/usr/bin/aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"{}'.format(target,location,self.mLogInfo.mLogType, self.mLogInfo.mLogGetFlag), shell=True)
            # subprocess.check_call('/usr/bin/aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*15'), shell=True)
            # subprocess.check_call('/usr/bin/aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*09'), shell=True)
            # subprocess.check_call('/usr/bin/aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"'.format(target,location,'core*18'), shell=True)


    def downWavFiles(self):
        yy = str(self.mLogInfo.mLogDate)[2:4]
        mm   = str(self.mLogInfo.mLogDate)[5:7]
        dd   = str(self.mLogInfo.mLogDate)[8:10]
        target = 's3://{}/uploads/audio/'.format(self.mLogInfo.mLogBucket) # 20170712 로그까지 유호

        # Folder setup
        if not os.path.exists(self.mLogInfo.mLogDirPath):
            subprocess.check_call('mkdir {}'.format(self.mLogInfo.mLogDirPath), shell=True)
        location = self.mLogInfo.mLogDirPath + '/' + self.mLogInfo.mLogcurrdate

        print '# [LogDownloader] target = %s' % target
        print '# [LogDownloader] location = %s' % location
        print '# [LogDownloader] sys.platform = %s' % sys.platform
        print '#----------------------------------------------------'
        if self.mIsFileWrite:
            self.mFp.write('# [LogDownloader] target = %s\n' % target)
            self.mFp.write('# [LogDownloader] location = %s\n' % location)
            self.mFp.write('# [LogDownloader] sys.platform = %s\n' % sys.platform)
            self.mFp.write('#----------------------------------------------------')
        subprocess.check_call('mkdir {}'.format(location), shell=True)

        if sys.platform is 'darwin':
            subprocess.check_call('aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"{}'.format(target,location,yy+mm+dd, self.mLogInfo.mLogGetFlag), shell=True)
        else:
            subprocess.check_call('/usr/bin/aws s3 cp {} {} --recursive --exclude "*" --include "*{}*"{}'.format(target,location,yy+mm+dd, self.mLogInfo.mLogGetFlag), shell=True)

    def getLogInfo(self):
        return self.mLogInfo

    def setfile(self,fp):
        self.mFp = fp
        self.mIsFileWrite = True
        print '[DailyLogWorker] mIsFileWrite = %s' % self.mIsFileWrite
        if self.mIsFileWrite:
            self.mFp.write('[DailyLogWorker] mIsFileWrite = %s\n' % self.mIsFileWrite)

    def closefile(self):
        # self.mFp.close()
        self.mIsFileWrite = False
        print '[DailyLogWorker] mIsFileWrite = %s' % self.mIsFileWrite
        if self.mIsFileWrite:
            self.mFp.write('[DailyLogWorker] mIsFileWrite = %s\n' % self.mIsFileWrite)


class LogInfo (object):

    def __init__(self):
        self.mLogDate = None
        self.mLogType = None
        self.mLogBucket = None
        self.mLogDirPath = None
        self.mLogAppKey = str()
        self.mLogGetFlag = None
        self.mLogTime = None
        self.mLogcurrdate=None

    def configLog(self,currdate,logtype,servertype,appkey):

        # 현재 schedule log만 날짜를 안받음 10 입력받음(고정값)

        self.mLogcurrdate = currdate
        self.mLogDate = date(int(currdate[0:4]),int(currdate[4:6]),int(currdate[6:8]))

        #schedule 파일명 포맷 YYYY.MM.DD.HH.MM.SS
        #if len(currdate)>8:
            #self.mLogTime = time(int(currdate[8:10]),int(currdate[10:12]),int(currdate[12:14]))
            #self.mLogDate = datetime.combine(self.mLogDate, self.mLogTime)

        if logtype:
            self.mLogType = logtype

        # Use '==' instead of 'is' (AUG 2017, SWKA)
        # because 'is' tests for object identity, and you have no guarantee that equal strings will use the same object.
        if self.mLogType == 'core':
            self.mLogDirPath = common.RAW_CORELOG_DIR
        elif self.mLogType == 'beacon':
            self.mLogDirPath = common.RAW_BEACONLOG_DIR
        elif self.mLogType == 'schedule':
            self.mLogDirPath = common.RAW_SCHEDULE_DIR
        elif self.mLogType == 'monitoring':
            self.mLogDirPath = common.RAW_MONITORING_DIR
        elif self.mLogType == 'active':
            self.mLogDirPath = common.RAW_ACTIVE_DIR
        elif self.mLogType == 'detect':
            self.mLogDirPath = common.RAW_DETECT_DIR
        elif self.mLogType == 'custom':
            self.mLogDirPath = common.RAW_CUSTOM_DIR
        elif self.mLogType == 'wav':
            self.mLogDirPath = common.RAW_WAV_FILES_DIR
        else:
            self.mLogDirPath = common.RAW_CORELOG_DIR

        if appkey.__len__() > 0:
            self.mLogAppKey = appkey
        else:
            self.mLogAppKey = str()

        #schedule 파일 다운로드는 v1 지원

        if servertype:
            if servertype == 's3': # s3 server use
                self.mLogBucket = 'soundlly.data'
                self.mLogGetFlag = ''
            elif servertype == 'dev': # dev server use
                self.mLogBucket = 'dev.soundlly.data'
                self.mLogGetFlag = ' --profile dev'

            elif servertype == 'v1':    #schedule of v1, which is in s3 sever use
                self.mLogBucket = 'bitsound.sdk.schedule'

            # another schedule format
            elif servertype == 'dev-schedule':
                self.mLogBucket = 'dev.bitsound.sdk.schedule'

            else:                     # default is s3 server
                self.mLogBucket = 'soundlly.data'
                self.mLogGetFlag = ''

        print '# [LogInfo] LogDate = %s' % self.mLogcurrdate
        print '# [LogInfo] LogType = %s' % self.mLogType
        print '# [LogInfo] LogDirPath = %s' % self.mLogDirPath
        print '# [LogInfo] LogBucket = %s' % self.mLogBucket
        print '# ------------------------------------------------#'
