from crontab import CronTab
from datetime import datetime
import json

import pandas
from dateutil import parser
from dateutil.rrule import *

def find_sub_freq(s,sub):
    val = ''
    if s.find(sub)>=0:
        start = s.find(sub)+len(sub)
        end = s.find(';',start)
        val = rec[start:end if end >0 else len(rec)]
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

request = {
    "endpoint": "creat_appointment",
    "remote_addr": "192.168.1.17",
    "form": {
        "values": [
#            "{\"recurrenceRule\":\"FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,SA,SU;INTERVAL=2;COUNT=5\",\"startDate\":\"2020-07-18T16:30:00.000Z\",\"endDate\":\"2020-07-18T17:00:00.000Z\",\"AllDay\":false,\"Text\":\"rec\",\"roomId\":1}"
            "{\"recurrenceRule\":\"FREQ=DAILY;INTERVAL=3\",\"startDate\":\"2020-07-18T16:30:00.000Z\",\"endDate\":\"2020-07-18T17:00:00.000Z\",\"AllDay\":false,\"Text\":\"freq\",\"roomId\":1}"
        ]
    },
    "headers": {
        "Referer": "http://localhost:3000/",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Content-Length": "229",
        "Accept-Language": "fr-fr",
        "Host": "gw:5000",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
        "Connection": "keep-alive",
        "Origin": "http://localhost:3000",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate"
    },
    "method": "POST",
    "data": {},
    "cookies": {},
    "args": {}
}

appoint = request['form']['values'][0]
japp = json.loads(appoint)
new_id = 10
japp['AppointmentId'] = new_id
row = pandas.DataFrame.from_records(japp, index=[japp['AppointmentId']])
print('row')
print(japp)

my_cron = CronTab(user='pi')
print('end "', row['endDate'].iloc[0],'"')
duree = parser.isoparse(row['endDate'].iloc[0]) - parser.isoparse(row['startDate'].iloc[0])
job = my_cron.new(command='python3 start_arrosage.py {} {}'.format(row["roomId"].iloc[0], duree.total_seconds() // 60) , comment='app{}'.format(row["AppointmentId"].iloc[0]))
job.setall(parser.isoparse(row['startDate'].iloc[0]))

if 'recurrenceRule' in japp.keys():
    rec = japp['recurrenceRule']
    set_reccure_cronjob(job,rec)
print(job)




exit(0)




my_cron = CronTab(user='pi')
found_job = False

for job in my_cron:
    print('job', job)
    if job.comment == 'test':
        found_job = True
        job.setall(datetime(2020, 7, 18, 10, 2))


if not(found_job) :
    job = my_cron.new(command='python3 /home/pi/Arrosage/pilot/writeDate.py', comment='test')
    job.setall(datetime(2020, 7, 18, 10, 2))

my_cron.write()

print (my_cron)