#!/bin/sh
# autoDownImportClipSchedule.sh
# Created by Chang Ho Lee  on 2017. 10.02
#
#
eval "$(pyenv init -)"
pyenv shell anaconda2-4.1.1

# python module path setup
export PYTHONPATH="${PYTHONPATH}:/mnt/coreLogs/CoreLogAnalysis/python_codes"

# python setAppkeyToClip.py

/home/haegol123/.pyenv/versions/anaconda2-4.1.1/bin/python /mnt/coreLogs/CoreLogAnalysis/runImportLog.py 10 -an clip -t schedule -s v1

