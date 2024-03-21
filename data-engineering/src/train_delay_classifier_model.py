import pandas as pd
import json
from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from pickle import dump, load
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.ensemble import RandomForestClassifier

class TrainDelayClassifier:
    
    def __init__(self, data_processor: DataPreprocessor):
        self.data_processor = data_processor
        self.split_train_test()
        self.create_model_perform_grid_search()
        
    def split_train_test(self):
        self.dataset = self.data_processor.dataset
        print(self.dataset.columns)
        self.y = self.dataset['is_late_arrival']
        self.X = self.dataset.drop('is_late_arrival', axis=1)
    
    def create_model_perform_grid_search(self):
        self.random_forest_classifier = RandomForestClassifier(n_estimators=10)
        
        self.shuffle_split = ShuffleSplit(n_splits=1, test_size=0.25)
        
        param_grid = {'max_depth': [2, 4, 6, 8, 10]}
        self.grid_search = GridSearchCV(self.random_forest_classifier, param_grid=param_grid, cv=self.shuffle_split, scoring='accuracy')
        self.grid_search.fit(self.X, self.y)
        
        print(f'Best parameters : {self.grid_search.best_params_}')
        print(f'Best score : {self.grid_search.best_score_}')
        
    
if __name__ == "__main__":
    
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    data_loader = DataLoader(trv_api_key, 1)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    data_processor = DataPreprocessor(train_announcements)
    trainDelayClassifier = TrainDelayClassifier(data_processor)

