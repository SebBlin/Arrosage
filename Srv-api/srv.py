from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS
from flask import jsonify
from my_utils import Arr_Appointment, save_request
import json
from pprint import pprint

app = Flask(__name__)

my_app = Arr_Appointment(filename='data.csv')

CORS(app, supports_credentials=True)

@app.route('/Get')
def get_appointment():
    return jsonify(my_app.get_all_data())

@app.route('/Post',methods=['POST'])
def creat_appointment():
    my_req = save_request(request)
    print ("request : ", json.dumps(my_req,indent=4))
    appoint = request.form['values']
    japp = json.loads(appoint)
    new_id = my_app.get_max_id()
    print('new ID : ', new_id)
    japp['AppointmentId'] = new_id
    my_app.add_app(japp)
    my_app.dump_data()
    return Response("", status=201, content_type=None)

@app.route('/Put',methods=['OPTIONS','PUT'])
def update_appointment():
    my_req = save_request(request)
    pprint(my_req)
    if 'values' in request.form.keys():
        appoint = request.form['values']
        japp = json.loads(appoint)
        my_app.update_app(japp)
        my_app.dump_data()
    return Response("", status=201, content_type=None)

@app.route('/Delete',methods=['OPTIONS','DELETE'])
def delete_appointment():
    my_req = save_request(request)
    pprint(my_req)
    if 'key' in request.form.keys():
        key = request.form['key']
        my_app.del_app(key)
        my_app.dump_data()

    return Response("", status=201, content_type=None)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')