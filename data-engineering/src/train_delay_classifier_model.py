import json
from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report

class TrainDelayClassifier:
    
    def __init__(self, data_processor: DataPreprocessor):
        self.data_processor = data_processor
        self.split_train_test()
        self.perform_grid_search()
        self.create_evaluate_model()
        
    def split_train_test(self):
        self.dataset = self.data_processor.dataset
        print(self.dataset.columns)
        self.y = self.dataset['is_late_arrival']
        self.X = self.dataset.drop('is_late_arrival', axis=1)
    
    def perform_grid_search(self):
        random_forest_classifier = RandomForestClassifier(n_estimators=10)
        
        shuffle_split = ShuffleSplit(n_splits=1, test_size=0.25)
        
        param_grid = {'max_depth': [2, 4, 6, 8, 10]}
        self.grid_search = GridSearchCV(random_forest_classifier, param_grid=param_grid, cv=shuffle_split, scoring='accuracy')
        self.grid_search.fit(self.X, self.y)
        
        print(f'Best parameters : {self.grid_search.best_params_}')
        print(f'Best score : {self.grid_search.best_score_}')
        
    def create_evaluate_model(self):
        ''' Creates & evaluates the Random forest model '''
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.25, random_state=42)
        
        self.random_forest_classifier = RandomForestClassifier(n_estimators=10, max_depth=self.grid_search.best_params_['max_depth'])
        self.random_forest_classifier.fit(X_train, y_train)
        y_pred = self.random_forest_classifier.predict(X_test)
        print(f'Accuracy {metrics.accuracy_score(y_test, y_pred)}')
        print(f'classification_report: \n{classification_report(y_test, y_pred)}')
    
if __name__ == "__main__":
    
    trv_api_key = 'REPLACE_IT_WITH_YOUR_API_KEY'
    num_days = 2
    data_loader = DataLoader(trv_api_key, num_days)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    data_processor = DataPreprocessor(train_announcements)
    trainDelayClassifier = TrainDelayClassifier(data_processor)
    
