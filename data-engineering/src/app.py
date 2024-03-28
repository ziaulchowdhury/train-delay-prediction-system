from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from train_delay_classifier_model import TrainDelayClassifier
from pickle import dump
import json
import os

def train_test_model(trv_api_key, num_days):
    print('Loading data ...')
    data_loader = DataLoader(trv_api_key, num_days)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'DONE! \nAnnouncement: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    print('Preprocessing data ...')
    data_processor = DataPreprocessor(train_announcements)
    
    print('Started training and predicting train delays ...')
    trainDelayClassifier = TrainDelayClassifier(data_processor)
    print('Done, prediction!')
    return trainDelayClassifier

def dump_model_weights(trainDelayClassifier):
    print('Dumping model weights to pkl file ...')
    dump(trainDelayClassifier, open('train_delay_classifier_weights.pkl', 'wb'))
    
if __name__ == "__main__":
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'

    download_data_num_days = os.environ['DOWNLOAD_DATA_NUM_DAYS']
    print(f'DOWNLOAD_DATA_NUM_DAYS: {download_data_num_days}, Int value: {int(download_data_num_days)}')
    # num_days = 2
    clf = train_test_model(trv_api_key, int(download_data_num_days))
    
    dump_model_weights(clf)
