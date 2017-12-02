#!/bin/sh
# filename: batchDownImportCustomLog.sh
# created by jaewook kang @ 2017 Aug

echo "Hello crontab">>/tmp/crontablog_rawCustomLog.txt
echo "user Custom logdown start">>/tmp/crontablog_rawCustomLog.txt

eval "$(pyenv init -)"
pyenv shell anaconda2-4.1.1

echo "pyenv success">>/tmp/crontablog_rawDetectLog_rawCustomLog.txt

i=$(date -d 'yesterday'  '+%y%m%d')
i='20'$i
echo " user Custom log down date ="${i}>>/tmp/crontablog_rawCustomLog.txt

# python module path setup
export PYTHONPATH="${PYTHONPATH}:/mnt/coreLogs/CoreLogAnalysis/python_codes"


/home/testcore/.pyenv/versions/anaconda2-4.1.1/bin/python /mnt/coreLogs/CoreLogAnalysis/runImportLog.py ${i} -an user -t custom -d
echo "log down and import success @ ="${i}>>/tmp/crontablog_rawCustomLog.txt
echo "-------End of user Custom logdown @="${i}>>/tmp/crontablog_rawCustomLog.txt

