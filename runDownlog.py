#-*- coding: utf-8 -*-
#!/usr/bin/python
#------------------------------------------------------------
# filename: runDownLog.py
# This is for Core performance measuring from bandend

# written by Jaewook Kang @ Mar 2017
#------------------------------------------------------------

import sys
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')

import intro
import downlog
import argparse

from appkeylist import APPKEY_FILENAME

appKeyFilename = APPKEY_FILENAME
appKeyfile = open(appKeyFilename,'r')
appKey = appKeyfile.readlines().pop()


# logtype = 'core'
# logtype = 'beacon'
logtype = 'detect'

# Log configureation
servertype = 's3'

intro.intro_DownLog()

# get logdate from input argument in the format of YYYYMMDD
parser = argparse.ArgumentParser()
parser.add_argument('logdate', help='date with format YYYYMMDD')
args = parser.parse_args()


downLogWorker = downlog.LogDownloader()
downLogWorker.setLogInfo(args.logdate,logtype,servertype,appKey)
downLogWorker.downLogRecord()




