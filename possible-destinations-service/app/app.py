#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:05:44 2024

@author: suhasini
"""
import logging
from flask import Flask, json, request
from flask_cors import CORS

# Init Flask Server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_train_schedule_data(source):
    train_schedules = [
        {"train_id": '874', "operational_train_number": "874", "operator": "SJ", "train_type": "PNA025", "from_location": "Cst", "to_location": "U", "advertised_time": "2024-03-19T00:26:00.000+01:00"},
        {"train_id": '346', "operational_train_number": "10346", "operator": "SJ", "train_type": "PNA045", "from_location": "De.ges", "to_location": "Cst", "advertised_time": "2024-03-19T04:35:00.000+01:00"},
        {"train_id": '322', "operational_train_number": "10322", "operator": "SJ", "train_type": "PNA025", "from_location": "Kac", "to_location": "G", "advertised_time": "2024-03-19T05:19:00.000+01:00"},
        {"train_id": '561', "operational_train_number": "561", "operator": "SJ", "train_type": "PNA026", "from_location": "Suc", "to_location": "Cst", "advertised_time": "2024-03-19T06:03:00.000+01:00"},
        {"train_id": '420', "operational_train_number": "420", "operator": "SJ", "train_type": "PNA026", "from_location": "G", "to_location": "Cst_1", "advertised_time": "2024-03-19T06:11:00.000+01:00"},
        {"train_id": '420', "operational_train_number": "420", "operator": "SJ", "train_type": "PNA026", "from_location": "G", "to_location": "Cst_2", "advertised_time": "2024-03-19T06:11:00.000+01:00"},
        {"train_id": '420', "operational_train_number": "420", "operator": "SJ", "train_type": "PNA026", "from_location": "G", "to_location": "Cst_3", "advertised_time": "2024-03-19T06:11:00.000+01:00"}
    ]
    ac_train = [schedule for schedule in train_schedules if schedule['from_location'] == source]
    logging.info(f"Filtered train schedules for source {source}: {ac_train}")
    return ac_train

@app.route('/v1/train-schedules', methods=['GET'])
def get_train_schedules():
    source = request.args.get('source')
    logging.info(f"Received request for train schedules from source: {source}")
    train_schedules = get_train_schedule_data(source)
    response = app.response_class(
        response=json.dumps(train_schedules),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=4999)
