#-*- coding: utf-8 -*-
#! /usr/bin/env python
#------------------------------------------------------------
# filename: beaconCount.py

# written by Jisu Choi @ Mar 2017
#------------------------------------------------------------

# 단말수, 시간 구간, 수신 시도 주기
import csv
import boto3
import botocore
import datetime
from ast import literal_eval
from slacker import Slacker

MAX_TRY_COUNT = 4
FILE_NAME_BASE = 'schedule'


class BeaconCount:
    def __init__(self, logdate, device_amount, period, app_key):
        self.logdate = logdate
        is_vlid_beacon = self.set_is_valid_beacon()
        self.is_valid_beacon_true = is_vlid_beacon['is_valid_beacon_true']
        self.is_valid_beacon_false = is_vlid_beacon['is_valid_beacon_false']
        self.device_amount = device_amount
        self.period = period
        self.app_key = app_key
        self.daily_schedule = {}
        self.schedule_times = self.set_schedule_times()
        self.beaconData = {}

    def set_is_valid_beacon(self):
        csv_file_name = 'csvfiles/dailyDataFrame/{}_beaconLog_DailyDataFrame.csv'.format(self.logdate)
        with open(csv_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            is_valid_beacon_true = 0
            is_valid_beacon_false = 0
            for row in reader:
                if row['isValidBeaconID'] == 'False':
                    is_valid_beacon_false += 1
                elif row['isValidBeaconID'] == 'True':
                    is_valid_beacon_true += 1
            return dict(is_valid_beacon_true=is_valid_beacon_true,
                        is_valid_beacon_false=is_valid_beacon_false)

    def set_beacon_data(self):
        csv_file_name = 'csvfiles/dailyDataFrame/{}_beaconLog_DailyDataFrame.csv'.format(self.logdate)
        with open(csv_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['beacon'] not in self.beaconData:
                    self.beaconData[row['beacon']] = []
                data_dict = dict(deviceTime=row['deviceTime'],
                                 isValidBeaconID=row['isValidBeaconID'])
                self.beaconData[row['beacon']].append(data_dict)

    def set_daily_schedule(self):
        schedules = self.get_schedule()
        for schedule in schedules:
            if schedule['beacon'] not in self.daily_schedule:
                self.daily_schedule[schedule['beacon']] = []
            self.daily_schedule[schedule['beacon']].append(schedule['time'])

    def get_try_receive_cnt(self):
        try_receive_cnt = (self.device_amount * self.schedule_times * MAX_TRY_COUNT)/self.period
        return try_receive_cnt

    def get_result(self):
        result = self.is_valid_beacon_false/self.get_try_receive_cnt()
        return str(result)[:3]

    def test(self):
        return self.is_valid_beacon_false

    def get_schedule(self):
        s3 = boto3.client('s3',
                          region_name='ap-northeast-1',
                          aws_access_key_id='AKIAJDN3647EA3YCRNIA',
                          aws_secret_access_key='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')
        bucket = 'bitsound.sdk.schedule'
        publisher_file_name = '{}/{}'.format(self.app_key, self.get_bucket_list_filename())
        try:
            resp = s3.get_object(Bucket=bucket, Key=publisher_file_name)
            chunk = resp['Body'].read(1024 * 8)
            if chunk:
                reader = literal_eval(chunk.decode('utf-8'))
                return reader['schedule']
        except botocore.exceptions.ClientError as e:
            return None

    def set_schedule_times(self):
        schedules = self.get_schedule()
        tiems = 0
        for schedule in schedules:
            for time in schedule['time']:
                time_str = time.split('/')
                start_time = datetime.datetime.strptime(time_str[0].split('+')[0], '%Y-%m-%dT%H:%M:%S')
                end_time = datetime.datetime.strptime(time_str[1].split('+')[0], '%Y-%m-%dT%H:%M:%S')
                result_time = (end_time-start_time).total_seconds()
                if result_time is not None:
                    tiems += result_time
        return tiems

    def slack_message_report(self):
        message_title = '{} Beacon Log Report'.format(self.logdate)
        message_test = '총 비콘 로그  : {} \n ' \
                       'Is valid True  : {} \n ' \
                       'Is valid False : {}'.format(self.is_valid_beacon_false + self.is_valid_beacon_true,
                                                   self.is_valid_beacon_true,
                                                   self.is_valid_beacon_false)
        slack = Slacker('xoxp-3445427460-147821815553-154436708035-2ccb1f17efe7c2e1d56ff3e2329fe59c')
        attachments = [{"pretext": message_title, "text": message_test, "color": "#7CD197"}]
        slack.chat.post_message('#core-log-report', attachments=attachments)

    def get_bucket_list_filename(self):
        results = []
        s3 = boto3.resource('s3',
                            region_name='ap-northeast-1',
                            aws_access_key_id='AKIAJDN3647EA3YCRNIA',
                            aws_secret_access_key='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')

        bucket = s3.Bucket('bitsound.sdk.schedule')
        for obj in bucket.objects.all():
            key = obj.key.split('/')
            if key[0] == self.app_key:
                if key[1][:19] == self.get_s3_schedule_date():
                    results.append(key[1])
        return results[-1]

    def get_s3_schedule_date(self):
        date = '{}.{}{}{}{}.{}{}.{}{}'.format('schedule',
                                              self.logdate[0],
                                              self.logdate[1],
                                              self.logdate[2],
                                              self.logdate[3],
                                              self.logdate[4],
                                              self.logdate[5],
                                              self.logdate[6],
                                              self.logdate[7],
                                              )
        return date

