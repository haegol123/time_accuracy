#-*- coding: utf-8 -*-
#!/usr/bin/python
#------------------------------------------------------------
# filename: resetAppKey.py
#
# written by Jaewook Kang and Soonwon Ka @ Mar 2017
#------------------------------------------------------------

import sys
from os import getcwd
sys.path.insert(0, getcwd()+'/python_codes')

from appkeylist import REG_CLiP_APPKEY_LIST, REG_CASH_APPKEY_LIST, APPKEY_FILENAME



appkeytxt = open(APPKEY_FILENAME,'r')
currAppKey = appkeytxt.readline()
appkeytxt.close()
print '#-----------------------------------------------------#'
print '# AppKey resetting module for coreLog analysis'
print '# Jaewook Kang @ 2017 MAR'
print '# ------------------------'
print '# The current App is %s' % currAppKey
isResetAppKey = raw_input('# Reset AppKey ? (y/n) >')
print '# ------------------------'
if isResetAppKey == 'y':
    print '> Choose AppName from the below list:'
    print '-1) CLiP'
    print '-2) CashSlide'
    while True:

        appname = raw_input('(1/2) >')
        appkeylist = []
        if appname == '1':
            appkeylist = REG_CLiP_APPKEY_LIST
            break
        elif appname == '2':
            appkeylist = REG_CASH_APPKEY_LIST
            break
        else:
            print '> Improper Input'

    print '> Select AppKey from the below list'
    for i in range(0,len(appkeylist)):
        print '%s) %s' %(i,appkeylist[i])

    while True:
        appkeynum = raw_input('>')
        if int(appkeynum) < len(appkeylist):
            break
        else:
            print '> Improper Input'

    currAppKey = appkeylist[int(appkeynum)]
    appkeytxt = open(APPKEY_FILENAME,'w')
    appkeytxt.truncate()
    appkeytxt.write(currAppKey)
    appkeytxt.close()


print '# The current App is set to %s' % currAppKey
print '# Good Bye !'
print '#-----------------------------------------------------#'

