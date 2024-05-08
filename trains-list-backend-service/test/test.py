import unittest
from unittest.mock import patch
import logging
from app import app, configure_swagger, get_train_schedule_data

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        configure_swagger(app)

    def test_configure_swagger(self):
        # Test that the Swagger UI blueprint is registered
        with self.app as client:
            response = client.get('/swagger-ui/')
            self.assertEqual(response.status_code, 200)

    @patch('app.get_train_schedule_data')
    def test_get_train_schedules(self, mock_get_train_schedule_data):
        # Test case 1: Valid source location
        mock_get_train_schedule_data.return_value = [
            {"train_id": '874', "operational_train_number": "874", "operator": "SJ", "train_type": "PNA025", "from_location": "Cst", "to_location": "U", "advertised_time": "2024-03-19T00:26:00.000+01:00"}
        ]
        response = self.app.get('/v1/train-schedules?source=Cst')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # Test case 2: Invalid source location
        mock_get_train_schedule_data.return_value = []
        response = self.app.get('/v1/train-schedules?source=InvalidLocation')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]')

    def test_get_train_schedule_data(self):
        # Test case 1: Valid source location
        train_schedules = get_train_schedule_data('Cst')
        self.assertIsInstance(train_schedules, list)
        self.assertGreater(len(train_schedules), 0)

        # Test case 2: Invalid source location
        train_schedules = get_train_schedule_data('InvalidLocation')
        self.assertEqual(len(train_schedules), 0)

        # Test case 3: Logging
        with self.assertLogs(level=logging.INFO) as cm:
            get_train_schedule_data('Cst')
            self.assertIn('Found train:', cm.output[0])
            self.assertIn('Filtered train schedules for source Cst:', cm.output[1])

if __name__ == '__main__':
    unittest.main()