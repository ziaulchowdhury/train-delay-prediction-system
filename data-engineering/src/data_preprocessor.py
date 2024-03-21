import pandas as pd
from data_loader import DataLoader
import json

class DataPreprocessor:
    
    def __init__(self, train_announcements):
        self.train_announcements = train_announcements
        self.preprocess_data()
        
    
    def preprocess_data(self):
        
        self.announcement_df = pd.DataFrame(train_announcements)
        
        self.announcement_dataset = pd.DataFrame()
        
        # Need one hot encoding
        self.announcement_dataset['activity_type'] = self.announcement_df['ActivityType']
        
        # Need one hot encoding
        self.announcement_dataset['train_id'] = self.announcement_df['AdvertisedTrainIdent']
        
        # Need one hot encoding
        self.announcement_dataset['operational_train_number'] = self.announcement_df['OperationalTrainNumber']
        
        # Need one hot encoding
        self.announcement_dataset['operator'] = self.announcement_df['Operator']
        
        # Get train type code from product information
        self.announcement_dataset['train_type'] = self.announcement_df.apply(lambda r : r.ProductInformation[0]['Code'], axis=1)
        
        # from location code
        self.announcement_dataset['from_location'] = self.announcement_df.apply(lambda r : r.FromLocation[0]['LocationName'], axis=1)
        
        # to location code
        self.announcement_dataset['to_location'] = self.announcement_df.apply(lambda r : r.ToLocation[0]['LocationName'], axis=1)
        
        self.add_time_features()
        
        # delay in seconds (based on time at location)
        self.announcement_dataset['delay_seconds'] = (pd.to_datetime(self.announcement_df['TimeAtLocation']) - pd.to_datetime(self.announcement_df['AdvertisedTimeAtLocation'])).dt.seconds
        self.announcement_dataset['delay_seconds'] = self.announcement_dataset['delay_seconds'].fillna(0)
        
        self.announcement_dataset['is_late_arrival'] = self.announcement_dataset.apply(lambda r : 1 if r['delay_seconds']/60 > 5 else 0, axis=1)
        
    def add_time_features(self):
        
        self.announcement_dataset['advertised_time_at_location'] = pd.to_datetime(self.announcement_df['AdvertisedTimeAtLocation'])
        
        self.announcement_dataset['advertised_year'] = self.announcement_dataset['advertised_time_at_location'].dt.year
        
        self.announcement_dataset['advertised_month'] = self.announcement_dataset['advertised_time_at_location'].dt.month
        
        self.announcement_dataset['advertised_day'] = self.announcement_dataset['advertised_time_at_location'].dt.day
        
        self.announcement_dataset['advertised_day_of_week'] = self.announcement_dataset['advertised_time_at_location'].dt.dayofweek
        
        self.announcement_dataset['advertised_is_weekend'] = (self.announcement_dataset['advertised_time_at_location'].dt.dayofweek >= 5).astype(int)
        
        self.announcement_dataset['advertised_season'] = (self.announcement_dataset['advertised_month'] % 12 + 3) // 3
        
        self.announcement_dataset['advertised_quarter'] = self.announcement_dataset['advertised_time_at_location'].dt.quarter
        
        self.announcement_dataset.drop(columns=['advertised_time_at_location'], inplace=True)
        
             
if __name__ == "__main__":
    
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    data_loader = DataLoader(trv_api_key, 1)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    data_processor = DataPreprocessor(train_announcements)
    data_processor.preprocess_data()
    
