#!/bin/sh
# batchDownImportCashDetectLog.sh
# Creatd by jwkang  on 2017. 8
#
# -----------using runImportlog.py ----------------
echo "Hello crontab">>/tmp/crontablog_rawCashDetectLog.txt
echo "user Cash logdown start">>/tmp/crontablog_rawCashDetectLog.txt

eval "$(pyenv init -)"
pyenv shell anaconda2-4.1.1

echo "pyenv success">>/tmp/crontablog_rawCashDetectLog.txt

i=$(date -d 'yesterday'  '+%y%m%d')
i='20'$i
echo " user Cash log down date ="${i}>>/tmp/crontablog_rawCashDetectLog.txt

# python module path setup
export PYTHONPATH="${PYTHONPATH}:/mnt/coreLogs/CoreLogAnalysis/python_codes"


/home/testcore/.pyenv/versions/anaconda2-4.1.1/bin/python /mnt/coreLogs/CoreLogAnalysis/runImportLog.py ${i} -an cash -t detect
echo "log down and import success @ ="${i}>>/tmp/crontablog_rawCashDetectLog.txt
echo "-------End of user Cash logdown @="${i}>>/tmp/crontablog_rawCashDetectLog.txt


##---------legacy (20170906 jwkang)---------------#
#echo "Hello crontab">>/tmp/crontablog_rawCashDetectLog.txt
#echo "user Cash logdown start">>/tmp/crontablog_rawCashDetectLog.txt
#
#eval "$(pyenv init -)"
#pyenv shell anaconda2-4.1.1
#echo "pyenv success">>/tmp/crontablog_rawCashDetectLog.txt
#
#
#python /mnt/coreLogs/CoreLogAnalysis/setAppkeyToCash.py
#i=$(date -d 'yesterday'  '+%y%m%d')
#i='20'$i
#echo " user Cash log down date ="${i}>>/tmp/crontablog_rawCashDetectLog.txt
#
### python module path setup
#export PYTHONPATH="${PYTHONPATH}:/mnt/coreLogs/CoreLogAnalysis/python_codes"
#
#
#/home/testcore/.pyenv/versions/anaconda2-4.1.1/bin/python  /mnt/coreLogs/CoreLogAnalysis/runDownlog.py ${i}
#/home/testcore/.pyenv/versions/anaconda2-4.1.1/bin/python  /mnt/coreLogs/CoreLogAnalysis/runImportDetectLog.py ${i}
#
#echo "log down and import success @ ="${i}>>/tmp/crontablog_rawCashDetectLog.txt
#echo "-------End of user Cash logdown @="${i}>>/tmp/crontablog_rawCashDetectLog.txt