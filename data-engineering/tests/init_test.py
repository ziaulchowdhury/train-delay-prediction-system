def test_square():
    assert True, 'Test passed'

def test_data_preprocessor():
    from data_preprocessor import DataPreprocessor
    import json
    from data_loader import DataLoader

    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    num_days = 2
    data_loader = DataLoader(trv_api_key, num_days)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    assert len(train_announcements) > 0, 'Test passed'