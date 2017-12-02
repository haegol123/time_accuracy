#!/bin/bash
# autoDownImportCashDetectLog.sh
# Creatd by jwkang  on 2017. 7. 31
#
#
eval "$(pyenv init -)"
pyenv shell anaconda2-4.1.1

# python module path setup
export PYTHONPATH="${PYTHONPATH}:/mnt/coreLogs/CoreLogAnalysis/python_codes"

python setAppkeyToCash.py
for i in {20170724..20170731}
do
echo " user Custom log down date ="$i
/home/testcore/.pyenv/versions/anaconda2-4.1.1/bin/python /mnt/coreLogs/CoreLogAnalysis/runImportLog.py $i -an cash -t detect


done
