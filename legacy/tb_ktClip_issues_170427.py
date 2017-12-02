#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: tb_ktClip_issues_170427.py
# This is for Core performance measuring from CoreLogs

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------


import sys
import time
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')



import downlog
import common as cm
import argparse

logTypeList = ['core', 'schedule','active']
logdate = '20170427'



#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: tb_kiclip_issues_170427.py
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



from appkeylist import APPKEY_FILENAME

isCSVwrite = True
isLogDown = True
# Log configureation
servertype = 's3'
frameSize = -1


# get appkey information
appKeyFilename = APPKEY_FILENAME
appKeyfile =  open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()
# logdate='20170422'
logdate = '20170331'

logtype = 'core'# 'core','active','schedule','beacon'가능


logDownWorker = downlog.LogDownloader()
logDownWorker.setLogInfo(logdate, logtype, servertype)
#logDownWorker.downLogRecord() # 이 주석을 풀면 로그 다운로드 기능을 포함한다
#
dailyDataFrameWorker = genDataFrame.DailyLogWorker()
dailyDataFrameWorker.init(logtype, logdate, appKey)             # logtype logdate appkey로 원하는 로그 정보를 초기화
dailyDataFrameWorker.makeDailyLogfileList()                     # 해당 날짜의 로그폴더에 다운로드된 로그 파일의 리스트를 생성

linenum = 0
while dailyDataFrameWorker.nextDailyLogFile():                   # 로그파일을 하나씩 브라우징 하는 루프
    dailyDataFrameWorker.loadDailyLog('grep')                    #  grep을 이용해서 로그 추출 (json load방식보다 매우 빠름
    currDataFrame = dailyDataFrameWorker.getDailyDataFrame(-1)   # 로그로 부터 데이터 프레임 생성
    linenum = linenum + dailyDataFrameWorker.mDataFrameForLog.getDataFrameSize() # 데이터 프레임의 라인수 카우트


print '%s Log linenum = %s' % (logtype, linenum)
