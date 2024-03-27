#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:05:44 2024

@author: chowdhuryz
"""

from flask import Flask, request, json
from prediction_request_preprocessor import PredictionRequestPreprocessor
from train_delay_prediction_model import TrainDelayPredictor
from pickle import load

from flask_restful import Api, Resource
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS, cross_origin

# Init Flask Server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def configure_swagger(app):
    ''' Configures Swagger API Documentation '''
    api = Api(app)

    SWAGGER_URL = '/swagger-ui'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "REST APIs of Train Delay Predictor Application"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def get_train_schedule_data():
    # Indices in train_announcement: 0, 4, 29, 39, 47
    train_schedules = [
        {"train_id": '874', "operational_train_number": "874", "operator": "SJ", "train_type": "PNA025", "from_location": "Cst", "to_location": "U", "advertised_time": "2024-03-19T00:26:00.000+01:00"},
        {"train_id": '346', "operational_train_number": "10346", "operator": "SJ", "train_type": "PNA045", "from_location": "De.ges", "to_location": "Cst", "advertised_time": "2024-03-19T04:35:00.000+01:00"},
        {"train_id": '322', "operational_train_number": "10322", "operator": "SJ", "train_type": "PNA025", "from_location": "Kac", "to_location": "G", "advertised_time": "2024-03-19T05:19:00.000+01:00"},
        {"train_id": '561', "operational_train_number": "561", "operator": "SJ", "train_type": "PNA026", "from_location": "Suc", "to_location": "Cst", "advertised_time": "2024-03-19T06:03:00.000+01:00"},
        {"train_id": '420', "operational_train_number": "420", "operator": "SJ", "train_type": "PNA026", "from_location": "G", "to_location": "Cst", "advertised_time": "2024-03-19T06:11:00.000+01:00"}
    ]
    return train_schedules

def load_request_preprocessor():
    request_preprocessor = PredictionRequestPreprocessor(
        'activity_type_label_encoder.pkl', 'train_id_label_encoder.pkl',
        'operational_train_number_label_encoder.pkl', 'operator_label_encoder.pkl',
        'train_type_label_encoder.pkl', 'from_location_label_encoder.pkl',
        'to_location_label_encoder.pkl')
    return request_preprocessor

def load_train_delay_predictor():
    clf = TrainDelayPredictor('train_delay_classifier_weights.pkl')
    return clf


@cross_origin()
@app.route('/v1/train-schedules', methods=['GET'])
def get_train_schedules():
    train_schedules = get_train_schedule_data()
    response = app.response_class(
        response=json.dumps(train_schedules),
        status=200,
        mimetype='application/json'
    )
    return response

@cross_origin()
@app.route('/v1/predict-train-delay', methods=['POST'])
def predict_train_delay():
    train_data = request.get_json()
    print(f'Request data: {train_data}')
    
    if not train_data or 'train_id' not in train_data:
        return jsonify({'error': 'Invalid request'}), 400
    
    train_id = train_data['train_id']
    operational_train_number = train_data['operational_train_number']
    operator = train_data['operator']
    train_type = train_data['train_type']
    from_location = train_data['from_location']
    to_location = train_data['to_location']
    advertised_time = train_data['advertised_time']
    
    X = request_preprocessor.preprocess_input(train_id, operational_train_number, operator, train_type, from_location, to_location, advertised_time)
    will_train_be_delayed = train_delay_predictor_clf.predict_will_train_be_delayed(X)
    print(f'Prediction response: {will_train_be_delayed}')
    
    response_str = ("Yes" if will_train_be_delayed[0] == 1 else "No")
    response_json = {"delay": response_str}
    
    response = app.response_class(
        response=json.dumps(response_json),
        status=200,
        mimetype='application/json'
    )
    return response


configure_swagger(app)

request_preprocessor = load_request_preprocessor()
train_delay_predictor_clf = load_train_delay_predictor()

if __name__ == '__main__':
    app.run(debug=True)
    
    