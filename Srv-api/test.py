import json
import pandas



filename = 'data.json'
with open(filename) as json_file:
    data = json.load(json_file)

data2 = {}
for a in data:
    print (a['AppointmentId'])
    data2[a['AppointmentId']]=a
print(a)