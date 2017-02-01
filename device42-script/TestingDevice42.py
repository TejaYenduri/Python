import unittest
import mock
from flask import json
from mock import patch
from Device42APIAccess import Device42Svc


class TestingDevice42(unittest.TestCase):
    def setUp(self):
        self.device42 = Device42Svc('credentials.cfg')

    @mock.patch('Device42APIAccess.requests.request')
    def test_get_building(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "buildings": [
                {
                    "address": "123 main st",
                    "building_id": 1,
                    "contact_name": "roger",
                    "contact_phone": "1234567890",
                    "custom_fields": [],
                    "name": "main office",
                    "notes": "super critical"
                }
            ]
        }
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/buildings/'
        response_dict = self.device42.get_method(url)
        print str(response_dict.json())
        mock_get.assert_called_once_with('GET', url, auth=('admin', 'adm!nd42'), verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)


if __name__ == '__main__':
    unittest.main()
