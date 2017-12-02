# -*- coding: utf-8 -*-

import sys
import csv
from os import getcwd
import argparse
import datetime

sys.path.insert(0,getcwd()+'/python_codes')


# get arguments from prompt
parser = argparse.ArgumentParser()

parser.add_argument('date', help='date with format YYYYMMDD')   #YYYYMMDD
parser.add_argument('-ch','--broadcastchannelname', help='type the name of the channels') # broadcastchannel name
args = parser.parse_args()
date = args.date
channel = args.broadcastchannelname


# paths that includes data files(schedule, monitoring)
basePath='csvfiles/dailyDataFrame'
monitoringPath='monitoring/monitoring'
schedulePath='schedule/schedule'

# file names(scheduleFilename, monitoringFilename)
scheduleFilename='_scheduleLog_schedule_DailyDataFrame.csv'
monitoringFilename='_monitoringLog_monitoring_DailyDataFrame.csv'
resultFilename='Accuracy_result_{}.csv'.format(date)    # YYYYMMDD

# total csv read
schedulefile = open('{}/{}/{}{}'.format(basePath,schedulePath,date,scheduleFilename), 'r') # schedule ,beacon,broadcastchannel,start,end
monitoringfile = open('{}/{}/{}{}'.format(basePath,monitoringPath,date,monitoringFilename),'r') # monitoring ,appKey,beacon,serverTime,phoneModel,sdkType

scheduleRdr = csv.reader(schedulefile)
monitoringRdr = csv.reader(monitoringfile)

#total monitoring Count
totalDetectCount=0
tmpCount=0

# row number 세기
resultRowNum = 0
tmpScheduleRowNum=0
rowNum=0


tmpDetectCount=0
tmpSwitch=0

# resultfile setting
resultList = []
scheduleCountList =[]
detectCountList=[]

########################### test
tmpDetectCountList=[]
# tmpDetectCountDic={}
# tmpB=0
tmpcolumn=0

# schedule Read     line4-> list
for line4 in scheduleRdr:
    print(line4)

# monitoring Read      line5-> list
for line5 in monitoringRdr:
    # 맨 윗줄에는 컬럼명이다
    if tmpcolumn == 0:
        tmpcolumn =1
        continue

    tmpB=line5[3]      #beacon
    if not any(d['beacon']==tmpB for d in tmpDetectCountList):  #tmpDetectCountList 에서 비콘값 이미 들어있는지 확인
        tmpDetectCountDic = dict(rowNum=rowNum, beacon=tmpB, monitoring_count=1)
        rowNum += 1
        tmpDetectCountList.append(tmpDetectCountDic)

    # beacon 값에 따라 저장 해두었으면 카운트만 증가
    else:
        # enumerate: index 값이랑 key 값 이름들을 뱉어낸다.
        for i, d in enumerate(tmpDetectCountList):
            if tmpDetectCountList[i]['beacon']==tmpB:  # count 0 이 아니면 1 증가
                tmpDetectCountList[i]['monitoring_count'] += 1

    tmpCount+=1
    print(line5)
totalDetectCount=tmpCount

# for tmplist in tmpDetectCount2:
#     try: tmpDetectCountDic[tmplist]+=1
#     except: tmpDetectCountDic[tmplist]=1
# print ("tmpDetectCountDic: {} \n").format(tmpDetectCountDic)


print('totalDetectConut: {} \n------------------------------------------------------------------------'.format(totalDetectCount))

schedulefile.close()
monitoringfile.close()

# schedulefile open for comparing
schedulefile = open('{}/{}/{}{}'.format(basePath,schedulePath,date,scheduleFilename), 'r') # schedule ,beacon,broadcastchannel,start,end
scheduleRdr = csv.reader(schedulefile)

# line-> list type
for scheduleLine in scheduleRdr:

    if scheduleLine[2] == channel:      # 명령행에서 입력 받은 채널과 예측 데이터의 채널이 일치하는 것을 먼저 걸러냄
        tmpBeacon = scheduleLine[1]

        tmpStart = scheduleLine[3]
        tmpEnd = scheduleLine[4]

        # Start Time Slice
        tmpStartYear= int(tmpStart[0:4])
        tmpStartMonth= int(tmpStart[5:7])
        tmpStartDay= int(tmpStart[8:10])
        tmpStartHour= int(tmpStart[11:13])
        tmpStartMinute= int(tmpStart[14:16])
        tmpStartSecond= int(tmpStart[17:19])

        # End Time Slice
        tmpEndYear= int(tmpEnd[0:4])
        tmpEndMonth= int(tmpEnd[5:7])
        tmpEndDay= int(tmpEnd[8:10])
        tmpEndHour= int(tmpEnd[11:13])
        tmpEndMinute= int(tmpEnd[14:16])
        tmpEndSecond= int(tmpEnd[17:19])

        startTime = datetime.datetime(tmpStartYear, tmpStartMonth, tmpStartDay, tmpStartHour, tmpStartMinute,
                                      tmpStartSecond)
        endTime = datetime.datetime(tmpEndYear, tmpEndMonth, tmpEndDay, tmpEndHour, tmpEndMinute,
                                    tmpEndSecond)

        # monitoring ,appKey,beacon,serverTime,phoneModel,sdkType 다시 읽어줘야됨
        monitoringfile = open('{}/{}/{}{}'.format(basePath, monitoringPath, date, monitoringFilename),
                  'r')
        monitoringRdr = csv.reader(monitoringfile)
        # schedule 데이터 에서 비콘 값 별로 count 하기
        if not any(d['beacon'] == scheduleLine[1] for d in
                   scheduleCountList):  # resultList에 담긴 dict 에서 beacon value를 찾자 (비교쓰고 for문 기입)
            schdic = dict(rowNum=tmpScheduleRowNum, beacon=scheduleLine[1], count=1)
            tmpScheduleRowNum += 1
            scheduleCountList.append(schdic)

        # beacon 값 있으면 해당 beacon 의 acuuracy를  증가 시킴
        else:
            # enumerate: index 값이랑 key 값 이름들을 뱉어낸다.
            for i, d in enumerate(scheduleCountList):
                if d['beacon'] == scheduleLine[1]:  # beacon값을 비교해서 beacon 값이 이미 있던 거면 accuracy 1 증가시킨다
                    scheduleCountList[i]['count'] += 1

        # monitoring beacon line by line, schedule beacon 값 기준으로 비교
        for monitoringLine in monitoringRdr:
            # if adid ==channel 비교 and beacon 비교 추가하기   ####################################################
            if tmpBeacon == monitoringLine[3]:     # schedule beacon 과 monitoring beacon 비교 str str 비교
                tmpDetect = monitoringLine[4]
                # if tmpSwitch<=totalDetectCount:
                #     # 측정 시간이 들어 맞았는지는 상관 없이 beacon 값에 따른 monitoring 로우 측정
                #     if not any(d['beacon'] == monitoringLine[2] for d in
                #             detectCountList):  # resultList에 담긴 dict 에서 beacon value를 찾자 (비교쓰고 for문 기입)
                #
                #         detdic = dict(rowNum=rowNum, beacon=monitoringLine[2], detect=1)
                #         rowNum += 1
                #         detectCountList.append(detdic)
                #
                # # beacon 값 있으면 해당 beacon 의 acuuracy를  증가 시킴
                #     else:
                #     # enumerate: index 값이랑 key 값 이름들을 뱉어낸다.
                #         for i, d in enumerate(detectCountList):
                #             if d['beacon'] == monitoringLine[2]:  # beacon값을 비교해서 beacon 값이 이미 있던 거면 accuracy 1증가시킨다
                #                 detectCountList[i]['detect'] += 1
                #                 tmpSwitch+=1
                #                 if tmpSwitch ==totalDetectCount:
                #                     tmpSwitch=0

                # tmpScheduleCount=1
                # print tmpScheduleCount
                # # detect time slice
                tmpDetectYear = int(tmpDetect[0:4])
                tmpDetectMonth = int(tmpDetect[5:7])
                tmpDetectDay = int(tmpDetect[8:10])
                tmpDetectHour = int(tmpDetect[11:13])
                tmpDetectMinute = int(tmpDetect[14:16])
                tmpDetectSecond = int(tmpDetect[17:19])

                # if not any(d['beacon'] == monitoringLine[2] for d in
                #            scheduleCountList):  # resultList에 담긴 dict 에서 beacon value를 찾자 (비교쓰고 for문 기입)
                #     tmpdic2 = dict(rowNum=rowNum, beacon=monitoringLine[2], ScheduleCount=1)
                #     rowNum += 1
                #     scheduleCountList.append(tmpdic2)
                #
                # # beacon 값 있으면 해당 beacon 의 accuracy를  증가 시킴
                # else:
                #     # enumerate: index 값이랑 key 값 이름들을 뱉어낸다.
                #     for i, d in enumerate(scheduleCountList):
                #         if d['beacon'] == monitoringLine[2]:  # beacon값을 비교해서 beacon 값이 이미 있던 거면 accuracy 1증가시킨다
                #             scheduleCountList[i]['ScheduleCount'] += 1

                detectTime = datetime.datetime(tmpDetectYear, tmpDetectMonth, tmpDetectDay, tmpDetectHour, tmpDetectMinute,
                                              tmpDetectSecond)
                # 측정 시간이 예측 시간 범위내에 있으면
                if endTime >= detectTime and startTime <= detectTime:

                    # 시간 계산 함수 짜기
                    print(scheduleLine)
                    print(monitoringLine)

                    # beacon 값 없으면 result 리스트에 새로운 사전형을 추가하겠다.
                    # def 함수:
                    #   for d in resultList
                    #       if d['beacon'] == monitoringLine[2]
                    #           return True
                    #       else:
                    #           return False
                    # 위의 함수를 불러다 씀
                    # if not any (def 함수 return이 False인 경우) # resultList의 beacon 값이 이전에 담겨있지 않으면
                    # ->        tmpdic
                    #           rownum
                    #           reusult.append
                    # else:                      # resultList 에 beacon 값이 담겨있다면
                    #
                    #           accuracy+1      # 정확도 카운트 1
                    #
                    if not any(d['beacon'] == monitoringLine[3] for d in resultList):   # resultList에 담긴 dict 에서 beacon value를 찾자 (비교쓰고 for문 기입)


                        tmpdic = dict(rowNum=resultRowNum, beacon=monitoringLine[3], correct=1)
                        resultRowNum += 1
                        resultList.append(tmpdic)

                    # beacon 값 있으면 해당 beacon 의 acuuracy를  증가 시킴
                    else:
                        # enumerate: index 값이랑 key 값 이름들을 뱉어낸다.
                        for i, d in enumerate(resultList):
                            if d['beacon'] == monitoringLine[3]:    # beacon값을 비교해서 beacon 값이 이미 있던 거면 accuracy 1증가시킨다
                                resultList[i]['correct'] += 1
                    # break;

            # else:
            #     tmpdic2= dict(beacon=tmpBeacon, schedulecount=tmpScheduleCount)
            #     tmpScheduleCount.append(tmpdic2)

print " correctresult : {} \n tmpSchedule(beacon 별 스케줄 데이터 개수) : {} \n detectCount : {} ".format(resultList,scheduleCountList,tmpDetectCountList)

schedulefile.close()
monitoringfile.close()

# dicts assemble
tmpdict={}
tmpdict2={}
# accuracy=0.0
tmpcorrect=0
tmpmonitoringcount=0

for i,d in enumerate(resultList):
    tmpdict=resultList[i]
    tmpdict2=tmpDetectCountList[i]
    tmpdict.update(tmpdict2)
    tmpcorrect=int(tmpdict['correct'])
    tmpmonitoringcount=int(tmpdict['monitoring_count'])
    accuracy=(float)(tmpcorrect)/tmpmonitoringcount*100.0
    accuracy=round(accuracy,2)
    d['accuracy']=accuracy
    print
print resultList,tmpcorrect,tmpmonitoringcount,


# csv write
with open('{}'.format(resultFilename),'w') as f:
    # Using dictionary keys as fieldnames for the CSV file header
    writer = csv.DictWriter(f, ['rowNum','beacon','correct','monitoring_count','accuracy'])
    writer.writeheader()

    for d in resultList:
        writer.writerow(d)
f.close()

