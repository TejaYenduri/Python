import unittest
import Device42APIAccess
import sys
import requests
import argparse


class TestingDevice42(unittest.TestCase):
    def setUp(self):
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('prog', default=Device42APIAccess.Device42Svc)
        parser.add_argument('filename', default='credentials.cfg')
        self.device42 = parser.parse_args()
        print type(self.device42)
        """
        self.device42 = Device42APIAccess.Device42Svc('credentials.cfg')

    def test_post_building(self):
        params_dict = {'name': 'building5'}
        response = self.device42.post_building(params_dict)
        print response.text
        self.assertEqual(response.status_code, 200)

    def test_post_building_exception(self):
        params_dict = {'building': 'building6'}
        self.assertRaises(requests.exceptions.RequestException, self.device42.post_building(params_dict))

    def test_delete_existing_entity(self):
        """
        Testing successful delete
        """
        param_id = ''
        response = self.device42.method_name(param_id)
        self.assertEqual(response.status_code, 200)

    def test_delete_nonExist_building(self):
        param_id = '7'
        self.assertRaises(requests.exceptions.RequestException, self.device42.method_name(param_id))

    def test_post_room(self):
        params_dict = {'name': 'room1', 'building': 'building6'}
        response = self.device42.post_room(params_dict)
        print response.text
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
