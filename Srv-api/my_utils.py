import json
import pandas
from crontab import CronTab
from datetime import datetime
import time
from dateutil import parser



class Arr_Appointment:
    def __init__(self,filename='data.json'):
        self.filename = filename
        self.load_data()
        self.crontab = CronTab(user='pi')

    def load_data(self):
        if self.filename:
            df = pandas.read_csv(self.filename, index_col=['idx'], skipinitialspace = True)
            self.data = df

    def dump_data(self):
        if self.filename:
            self.data.to_csv(self.filename, index_label="idx")
    
    def get_max_id(self):
        midx = self.data.index.max()
        midx = 0 if pandas.isna(midx) else midx
        return midx + 1
    
    def get_all_data(self): 
        s = self.data.to_json(orient='records')
        j = json.loads(s)
        return j

    def add_app(self, app):
        print(app)
        print(type(app))
        row = pandas.DataFrame.from_records(app, index=[app['AppointmentId']])
        print("after row")
        print(row)
        if row.any(axis=None):
            print('add row')
            self.data = self.data.append(row,sort=False)
            print('end "', row['endDate'].iloc[0],'"')
            duree = parser.isoparse(row['endDate'].iloc[0]) - parser.isoparse(row['startDate'].iloc[0])
            job = self.crontab.new(command='/usr/bin/python3 /home/pi/Arrosage/pilot/start_arrosage.py {} {}'.format(row["roomId"].iloc[0], int(duree.total_seconds() // 60)) , comment='app{}'.format(int(row["AppointmentId"].iloc[0])))
            job.setall(parser.isoparse(row['startDate'].iloc[0]))
            if 'recurrenceRule' in row.columns:
                set_reccure_cronjob(job,row['recurrenceRule'].iloc[0])
            print(job)
            self.crontab.write()
        print(self.data)
        
    def update_app(self, app):
        print(" start update")
        print(app)
        row = pandas.DataFrame.from_records(app, index=[app['AppointmentId']])
        job_iter = self.crontab.find_comment('app{}'.format(row["AppointmentId"].iloc[0]))
        job = next(job_iter)
        print(self.data.index)
        self.data.update(row)
        duree = parser.isoparse(row['endDate'].iloc[0]) - parser.isoparse(row['startDate'].iloc[0])
        job.set_command('/usr/bin/python3 /home/pi/Arrosage/pilot/start_arrosage.py {} {}'.format(row["roomId"].iloc[0], int(duree.total_seconds() // 60)))
        job.setall(parser.isoparse(row['startDate'].iloc[0]))
        if 'recurrenceRule' in row.columns and row['recurrenceRule'].iloc[0] :
            set_reccure_cronjob(job,row['recurrenceRule'].iloc[0])
        print(job)
        self.crontab.write()
        print(self.data)

    def del_app(self, key):
        print(int(key))
        self.data.drop(index=int(key), axis=0, inplace=True)
        self.crontab.remove_all(comment='app{}'.format(key))
        self.crontab.write()
        print(self.data)


########################
# Other 

from flask import Flask, request, Response, g

def save_request(request):
    req_data = {}
    req_data['endpoint'] = request.endpoint
    req_data['method'] = request.method
    req_data['cookies'] = dict(request.cookies)
    req_data['data'] = dict(request.data)
    req_data['headers'] = dict(request.headers)
    req_data['headers'].pop('Cookie', None)
    req_data['args'] = dict(request.args)
    req_data['form'] = dict(request.form)
    req_data['remote_addr'] = request.remote_addr
    return req_data


def find_sub_freq(s,sub):
    val = ''
    if s.find(sub)>=0:
        start = s.find(sub)+len(sub)
        end = s.find(';',start)
        val = s[start:end if end >0 else len(s)]
    return val

def set_reccure_cronjob(job,rec):
    print(rec)
    f_FREQ = find_sub_freq(rec,'FREQ=')
    f_INTERVAL = find_sub_freq(rec,'INTERVAL=')
    f_BYDAY = find_sub_freq(rec,'BYDAY=')

    map_dow = {'MO':'mon','TU':'tue','WE':'wed','TH':'thu','FR':'fri','SA':'sat','SU':'sun'}

    if f_FREQ == 'DAILY':
        intervall = 1
        if f_INTERVAL != '':
            intervall = f_INTERVAL
        job.day.every(intervall)
        job.month.every(1)
    if f_FREQ == 'WEEKLY':
        intervall = 1
        if f_BYDAY != '':
            malist = list(map(lambda x: map_dow[x],f_BYDAY.split(',')))
            job.day.every(1)
            job.month.every(1)
            job.dow.on(*malist)
