import pandas as pd
from data_loader import DataLoader
import json
from sklearn import preprocessing
from pickle import dump

class DataPreprocessor:
    
    def __init__(self, train_announcements):
        self.train_announcements = train_announcements
        self.preprocess_data()
        
    def preprocess_data(self):
        ''' Creates feature set from train announcements and does label encoding and dumps encoder classes to files '''
        self.create_feature_set()
        self.encode_features()
        self.dump_label_encoders()
        
    
    def create_feature_set(self):
        ''' Creates feature set from train_announcements '''
        self.announcement_dataset = pd.DataFrame()
        self.announcement_df = pd.DataFrame(self.train_announcements)
        
        self.announcement_dataset['activity_type'] = self.announcement_df['ActivityType']
        self.announcement_dataset['train_id'] = self.announcement_df['AdvertisedTrainIdent']
        self.announcement_dataset['operational_train_number'] = self.announcement_df['OperationalTrainNumber']
        self.announcement_dataset['operator'] = self.announcement_df['Operator']
        self.announcement_dataset['train_type'] = self.announcement_df.apply(lambda r : r.ProductInformation[0]['Code'], axis=1)
        self.announcement_dataset['from_location'] = self.announcement_df.apply(lambda r : r.FromLocation[0]['LocationName'], axis=1)
        self.announcement_dataset['to_location'] = self.announcement_df.apply(lambda r : r.ToLocation[0]['LocationName'], axis=1)
        
        self.add_time_features()
        
        # delay in seconds (based on time at location)
        self.announcement_dataset['delay_seconds'] = (pd.to_datetime(self.announcement_df['TimeAtLocation']) - pd.to_datetime(self.announcement_df['AdvertisedTimeAtLocation'])).dt.seconds
        self.announcement_dataset['delay_seconds'] = self.announcement_dataset['delay_seconds'].fillna(0)
        
        # Label (1 = delay, 0 = on time)
        self.announcement_dataset['is_late_arrival'] = self.announcement_dataset.apply(lambda r : 1 if r['delay_seconds']/60 > 5 else 0, axis=1)
        
    def add_time_features(self):
        ''' Add time features based on AdvertisedTimeAtLocation '''
        self.announcement_dataset['advertised_time_at_location'] = pd.to_datetime(self.announcement_df['AdvertisedTimeAtLocation'])
        self.announcement_dataset['advertised_year'] = self.announcement_dataset['advertised_time_at_location'].dt.year
        self.announcement_dataset['advertised_month'] = self.announcement_dataset['advertised_time_at_location'].dt.month
        self.announcement_dataset['advertised_day'] = self.announcement_dataset['advertised_time_at_location'].dt.day
        self.announcement_dataset['advertised_hour'] = self.announcement_dataset['advertised_time_at_location'].dt.hour
        self.announcement_dataset['advertised_minute'] = self.announcement_dataset['advertised_time_at_location'].dt.minute
        self.announcement_dataset['advertised_day_of_week'] = self.announcement_dataset['advertised_time_at_location'].dt.dayofweek
        self.announcement_dataset['advertised_is_weekend'] = (self.announcement_dataset['advertised_time_at_location'].dt.dayofweek >= 5).astype(int)
        self.announcement_dataset['advertised_season'] = (self.announcement_dataset['advertised_month'] % 12 + 3) // 3
        self.announcement_dataset['advertised_quarter'] = self.announcement_dataset['advertised_time_at_location'].dt.quarter
        self.announcement_dataset.drop(columns=['advertised_time_at_location'], inplace=True)
    
    def encode_features(self):
        ''' Encodes categorical values with label encoding'''
        self.dataset = self.announcement_dataset.copy(deep=False)
        
        self.activity_type_label_encoder = preprocessing.LabelEncoder()
        self.dataset['activity_type'] = self.activity_type_label_encoder.fit_transform(self.dataset['activity_type'])
        
        self.train_id_label_encoder = preprocessing.LabelEncoder()
        self.dataset['train_id'] = self.train_id_label_encoder.fit_transform(self.dataset['train_id'])
        
        self.operational_train_number_label_encoder = preprocessing.LabelEncoder()
        self.dataset['operational_train_number'] = self.operational_train_number_label_encoder.fit_transform(self.dataset['operational_train_number'])
        
        self.operator_label_encoder = preprocessing.LabelEncoder()
        self.dataset['operator'] = self.operator_label_encoder.fit_transform(self.dataset['operator'])
        
        self.train_type_label_encoder = preprocessing.LabelEncoder()
        self.dataset['train_type'] = self.train_type_label_encoder.fit_transform(self.dataset['train_type'])
        
        self.from_location_label_encoder = preprocessing.LabelEncoder()
        self.dataset['from_location'] = self.from_location_label_encoder.fit_transform(self.dataset['from_location'])
        
        self.to_location_label_encoder = preprocessing.LabelEncoder()
        self.dataset['to_location'] = self.to_location_label_encoder.fit_transform(self.dataset['to_location'])
        
        
    def dump_label_encoders(self):
        ''' Dumps label encoders to pickel file for reloading them later '''
        dump(self.activity_type_label_encoder, open('activity_type_label_encoder.pkl', 'wb'))
        dump(self.train_id_label_encoder, open('train_id_label_encoder.pkl', 'wb'))
        dump(self.operational_train_number_label_encoder, open('operational_train_number_label_encoder.pkl', 'wb'))
        dump(self.operator_label_encoder, open('operator_label_encoder.pkl', 'wb'))
        dump(self.train_type_label_encoder, open('train_type_label_encoder.pkl', 'wb'))
        dump(self.from_location_label_encoder, open('from_location_label_encoder.pkl', 'wb'))
        dump(self.to_location_label_encoder, open('to_location_label_encoder.pkl', 'wb'))

             
if __name__ == "__main__":
    
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    data_loader = DataLoader(trv_api_key, 1)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    data_processor = DataPreprocessor(train_announcements)    
