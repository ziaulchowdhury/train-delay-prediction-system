#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:29:33 2024

@author: chowdhuryz
"""

import pandas as pd
from pickle import load

class PredictionRequestPreprocessor:
    
    def __init__(self, activity_type_label_encoder_path,train_id_label_encoder_path, 
                 operational_train_number_label_encoder_path, operator_label_encoder_path, 
                 train_type_label_encoder_path, from_location_label_encoder_path, 
                 to_location_label_encoder_path):
        
        self.activity_type_label_encoder = self.load_encoder(activity_type_label_encoder_path)
        self.train_id_label_encoder = self.load_encoder(train_id_label_encoder_path)
        self.operational_train_number_label_encoder = self.load_encoder(operational_train_number_label_encoder_path)
        self.operator_label_encoder = self.load_encoder(operator_label_encoder_path)
        self.train_type_label_encoder = self.load_encoder(train_type_label_encoder_path)
        self.from_location_label_encoder = self.load_encoder(from_location_label_encoder_path)
        self.to_location_label_encoder = self.load_encoder(to_location_label_encoder_path)
    
    def load_encoder(self, encoder_file_name):
        opened_file = open('../model-weights/' + encoder_file_name, 'rb')
        return load(opened_file)

    def preprocess_input(self, train_id, operational_train_number, operator, 
                        train_type, from_location, to_location, advertised_time):
        ''' Creates feature set from train announcements and does label encoding and dumps encoder classes to files '''
        
        self.activity_type = 'Ankomst'
        self.train_id = train_id
        self.operational_train_number = operational_train_number
        self.operator = operator
        self.train_type = train_type
        self.from_location = from_location
        self.to_location = to_location
        self.advertised_time = advertised_time
        
        self.X = pd.DataFrame()
            
        self.create_feature_set()
        
        return self.X
        
    
    def create_feature_set(self):
        ''' Creates feature set from train_announcements '''
        
        self.X['activity_type'] = self.activity_type_label_encoder.transform([self.activity_type])
        self.X['train_id'] = self.train_id_label_encoder.transform([self.train_id])
        self.X['operational_train_number'] = self.operational_train_number_label_encoder.transform([self.operational_train_number])
        self.X['operator'] = self.operator_label_encoder.transform([self.operator])
        self.X['train_type'] = self.train_type_label_encoder.transform([self.train_type])
        self.X['from_location'] = self.from_location_label_encoder.transform([self.from_location])
        self.X['to_location'] = self.to_location_label_encoder.transform([self.to_location])
        
        self.add_time_features()
        
        # delay is 0 as we don't know it
        self.X['delay_seconds'] = [0]
        
        
    def add_time_features(self):
        ''' Add time features based on AdvertisedTimeAtLocation '''
        
        self.X['advertised_time_at_location'] = [pd.to_datetime(self.advertised_time)]
        
        self.X['advertised_year'] = self.X['advertised_time_at_location'].dt.year
        self.X['advertised_month'] = self.X['advertised_time_at_location'].dt.month
        self.X['advertised_day'] = self.X['advertised_time_at_location'].dt.day
        self.X['advertised_hour'] = self.X['advertised_time_at_location'].dt.hour
        self.X['advertised_minute'] = self.X['advertised_time_at_location'].dt.minute
        self.X['advertised_day_of_week'] = self.X['advertised_time_at_location'].dt.dayofweek
        self.X['advertised_is_weekend'] = (self.X['advertised_time_at_location'].dt.dayofweek >= 5).astype(int)
        self.X['advertised_season'] = (self.X['advertised_month'] % 12 + 3) // 3
        self.X['advertised_quarter'] = self.X['advertised_time_at_location'].dt.quarter
        
        self.X.drop(columns=['advertised_time_at_location'], inplace=True)

