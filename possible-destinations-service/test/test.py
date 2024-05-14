import unittest
from unittest.mock import patch
from app import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_train_schedule_data')
    def test_get_train_schedules(self, mock_get_train_schedule_data):
        mock_get_train_schedule_data.return_value = [
            {"train_id": '123', "operational_train_number": "123", "operator": "TestOperator", "train_type": "TestType", "from_location": "TestSource", "to_location": "TestDestination", "advertised_time": "2024-05-14T12:00:00.000+01:00"}
        ]
        response = self.app.get('/v1/train-schedules?source=TestSource')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['train_id'], '123')

    def test_missing_source_param(self):
        response = self.app.get('/v1/train-schedules')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
