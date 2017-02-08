import unittest
import responses

import mock
from Device42APIAccess import Device42Svc

device42 = Device42Svc('credentials.cfg')


class TestingDevice42(unittest.TestCase):
    def setUp(self):
        # self.device42 = Device42Svc('credentials.cfg')
        pass

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
        response_dict = device42.get_method(url)
        mock_get.assert_called_once_with('GET', url, auth=('admin', 'adm!nd42'), verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.request')
    def test_get_room(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "rooms": [
                {
                    "building": "main office",
                    "building_id": 1,
                    "custom_fields": [],
                    "name": "2nd Floor",
                    "notes": "super critical",
                    "room_id": 1
                }
            ]
        }
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/rooms/'
        response_dict = device42.get_all_rooms()
        mock_get.assert_called_once_with('GET', url, auth=('admin', 'adm!nd42'), verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_building(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "msg": ["Building added/updated successfully", 4, "main office"],
            "code": 0
        }
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/buildings/'
        payload = {'name': 'TestBuilding'}
        response_dict = device42.post_building(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_room(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "msg": ["Room added successfully", 7, "TestRoom"],
            "code": 0
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/rooms/'
        payload = {'name': 'TestRoom', 'building_id': 4}
        response_dict = device42.post_room(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @responses.activate
    def test_post_room_with_building(self):
        responses.add(responses.POST, 'https://10.0.0.12/api/1.0/rooms/',
                      body='[{"msg": ["Room added successfully", 7, "TestRoom"], "code": 0}]',
                      content_type="application/json",
                      status=200)
        responses.add(responses.GET, 'https://10.0.0.12/api/1.0/buildings/',
                      body='{"buildings": [{"address": "879 main st", "building_id": 4,'
                           '"contact_name": "roger","contact_phone": "1234567890","custom_fields": [], '
                           '"groups": "Prod_East:no, Corp:yes", "name": "Test Building", "notes": "super critical"}]}',
                      content_type="application/json",
                      status=200)
        payload = {'name': 'TestRoom', 'building': 'Test Building'}
        response = device42.post_room(payload)
        assert response.json() == [{
            "msg": ["Room added successfully", 7, "TestRoom"],
            "code": 0
        }]

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_rack(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "msg": ["rack added.", 29, "34"],
            "code": 0
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/racks/'
        payload = {'name': 'TestRack', 'size': 42}
        response_dict = device42.post_rack(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_hardware(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "msg": ["hardware model added or updated", 1, "PE 1950"],
            "code": 0
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/hardwares/'
        payload = {'name': 'TestHardware'}
        response_dict = device42.post_hardware_model(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_device_rack(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {
            "msg": ["device added or updated in the rack", 2, "[2.0] - RA1 -1st floor"],
            "code": 0
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/device/rack/'
        payload = {'device': 'nh-switch-01', 'rack_id': 29, 'start_at': 2}
        response_dict = device42.post_device_rack(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)

    @mock.patch('Device42APIAccess.requests.post')
    def test_post_device(self, mock_get):
        mock_response = mock.Mock()
        expected_dict = {"msg": ["device added or updated", 46, "db-080-westport", 'true', 'true'], "code": 0}
        mock_response.status_code = 200
        mock_response.json.return_value = expected_dict
        mock_get.return_value = mock_response
        url = 'https://10.0.0.12/api/1.0/devices/'
        payload = {'name': 'db-080-westport'}
        response_dict = device42.post_device(payload=payload)
        mock_get.assert_called_once_with(url, auth=('admin', 'adm!nd42'), data=payload, verify=False)
        self.assertEqual(1, mock_get.call_count)
        self.assertEqual(response_dict.json(), expected_dict)


if __name__ == '__main__':
    unittest.main()
