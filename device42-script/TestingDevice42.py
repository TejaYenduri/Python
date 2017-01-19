import unittest
import Device42APIAccess


class TestingDevice42(unittest.TestCase):
    def setUp(self):
        self.device42 = Device42APIAccess.Device42Svc('credentials.cfg')

    def test_get_building(self):
        response = self.device42.get_all_buildings()
        print response


"""
    def test_post_building(self):
        params_dict = {'name': 'building5'}
        response = self.device42.post_building(params_dict)
        print response.text
        self.assertEqual(response.status_code, 200)

    def test_post_building_exception(self):
        params_dict = {'building': 'building6'}
        self.assertRaises(requests.exceptions.RequestException, self.device42.post_building(params_dict))

    def test_delete_existing_building(self):

        Testing successful delete

        param_id = ''
        response = self.device42.delete_building(param_id)
        self.assertEqual(response.status_code, 200)

    def test_delete_nonExist_building(self):
        param_id = '7'
        self.assertRaises(requests.exceptions.RequestException, self.device42.delete_building(param_id))

    def test_post_room(self):
        params_dict = {'name': 'room1', 'building': 'building6'}
        response = self.device42.post_room(params_dict)
        print response.text
        self.assertEqual(response.status_code, 200)

    def test_post_room_exception(self):
        params_dict = {'room': 'room1', 'building': 'building6'}
        self.assertRaises(requests.exceptions.RequestException, self.device42.post_room(params_dict))

    def test_post_rack(self):
        params_dict = {'rack': 'rack1', 'room': 'room1', 'building': 'building6'}
        response = self.device42.post_rack(params_dict)
        print response.text
        self.assertEqual(response.status_code, 200)

    def test_post_rack_exception(self):
        params_dict = {'rack': 'rack1', 'room': 'room1'}
        self.assertRaises(requests.exceptions.RequestException, self.device42.post_rack(params_dict))

"""
if __name__ == '__main__':
    unittest.main()
