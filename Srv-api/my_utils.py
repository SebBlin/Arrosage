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
        midx = 1 if pandas.isna(midx)
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
            self.data = self.data.append(row)
            print('end "', row['endDate'].iloc[0],'"')
            duree = parser.isoparse(row['endDate'].iloc[0]) - parser.isoparse(row['startDate'].iloc[0])
            job = self.crontab.new(command='python3 start_arrosage.py {} {}'.format(row["roomId"].iloc[0], duree.total_seconds() // 60) , comment='app{}'.format(row["AppointmentId"].iloc[0]))
            print(job)
        print(self.data)
        
    def update_app(self, app):
        print(" start update")
        print(app)
        row = pandas.DataFrame.from_records(app, index=[app['AppointmentId']])
        print(self.data.index)
        self.data.update(row)
        # row = pandas.DataFrame.replace(value=app, index=[app['AppointmentId']])
        print(self.data)

    def del_app(self, key):
        print(int(key))
        self.data.drop(index=int(key), axis=0, inplace=True)
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


