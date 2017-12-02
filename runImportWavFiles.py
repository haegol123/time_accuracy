#-*- coding: utf-8 -*-
#!/usr/bin/python
#------------------------------------------------------------
# filename: runImportWavFiles.py
# written by Soonwon Ka @ Aug 2017
#------------------------------------------------------------
import sys
from os import getcwd
sys.path.insert(0,getcwd()+'/python_codes')

import downlog
import genDataFrame
import common as cm
from datetime import datetime
import intro
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

import argparse
import subprocess
from appkeylist import APPKEY_FILENAME, AppkeyList

# Log config
logtype = 'wav'

# if FrameSize == -1, take all items from the log
frameSize = -1

# intro
intro.intro_ImportWav()

# get logdate from prompt
parser = argparse.ArgumentParser()
parser.add_argument('-an','--appname', default='clip', help='set the appname') # default 'clip'
parser.add_argument('logdate', help='date with format YYYYMMDD')
parser.add_argument('-d','--dev', action='store_true', help='use dev server')
args = parser.parse_args()

# get appkey information
aklist = AppkeyList()
aklist.setAppkeyList(args.appname)
appname = args.appname
appKey = aklist.getAppkey()

# Server setup
servertype = 's3'
if args.dev:
    servertype = 'dev'

print '# [runImportWavFiles] ------------------------------------------------------'
print '#   Log date: %s' % args.logdate
print '#   Server type: %s' % servertype
downLogWorker = downlog.LogDownloader()
downLogWorker.setLogInfo(args.logdate,logtype,servertype)
downLogWorker.downWavFiles()
print '# [runImportWavFiles] ------------------------------------------------------'
