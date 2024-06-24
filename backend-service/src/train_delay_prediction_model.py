#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:06:42 2024
@author: chowdhuryz
"""

from prediction_request_preprocessor import PredictionRequestPreprocessor
from pickle import load

class TrainDelayPredictor:
    
    def __init__(self, model_weight_path):
        self.model_weight_path = model_weight_path
        self.load_model()
        
    def load_model(self):
        self.train_delay_clf = load(open('../model-weights/' + self.model_weight_path, 'rb'))
    
    def predict_will_train_be_delayed(self, X):
        will_train_be_delayed = self.train_delay_clf.predict(X)
        return will_train_be_delayed
    
if __name__ == "__main__":
    request = PredictionRequestPreprocessor(
        'activity_type_label_encoder.pkl', 'train_id_label_encoder.pkl',
        'operational_train_number_label_encoder.pkl', 'operator_label_encoder.pkl',
        'train_type_label_encoder.pkl', 'from_location_label_encoder.pkl',
        'to_location_label_encoder.pkl')
    X = request.preprocess_input('874', '874', 'SJ', 'PNA025', 'Cst', 'U', '2024-03-19T00:26:00.000+01:00')
    
    clf = TrainDelayPredictor('train_delay_classifier_weights.pkl')
    will_train_be_delayed = clf.predict_will_train_be_delayed(X)
    print(f'Prediction: {will_train_be_delayed}')
    