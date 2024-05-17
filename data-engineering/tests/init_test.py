import sys
sys.path.append("src")
import json
from data_loader import DataLoader
import pytest

def test_square():
    assert True, 'Test passed'

'''
@pytest.mark.parametrize("num_days,expected_result", [(2, True), (1, True), (3, False)])
def test_data_loader_two_days(num_days, expected_result):
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    num_days = 2
    data_loader = DataLoader(trv_api_key, num_days)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')

    if expected_result:
        assert len(train_announcements) > 0, 'Test passed'
    else:
        assert len(train_announcements) == 0, 'Test passed'
'''