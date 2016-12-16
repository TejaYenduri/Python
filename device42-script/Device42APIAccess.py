import ConfigParser
import requests

BASE_URL = 'https://172.20.5.47'
BUILDINGS_URL = BASE_URL + "//api/1.0/buildings/"
ROOMS_URL = BASE_URL + "/api/1.0/rooms/"
DEVICES_URL = BASE_URL + '/api/1.0/devices/'

"""

"""


class Device42Svc:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read('credentials.cfg')
        self.user = config.get('credentials', 'USER')
        self.password = config.get('credentials', 'PASSWORD')

    def get_all_buildings(self):
        """
        Getting all buildings information
        """
        try:
            response = requests.get(BUILDINGS_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def get_all_rooms(self):
        """
        Getting all rooms information from device42 application using get request
        """
        try:
            response = requests.get(ROOMS_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def get_all_devices(self):
        """
        Getting all devices information from device42 application using get request
        """
        try:
            response = requests.get(DEVICES_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def post_building(self, payload):
        """
        Create a building with given data in device42 using POST
        """
        try:
            if bool(payload) and 'name' in payload:
                response = requests.post(BUILDINGS_URL, auth=(self.user, self.password), verify=False, data=payload)
                print response.text
            else:
                print "invalid data"
        except requests.exceptions.RequestException as err:
            print err

    def post_room(self, payload):
        """
        Create a room with given data in device42 using POST
        """
        try:
            response = requests.post(ROOMS_URL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def post_device(self, payload):
        """
        Create a device with given data in device42 using POST
        """
        try:
            response = requests.post(DEVICES_URL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
        except requests.exceptions.RequestException as err:
            print err


d42 = Device42Svc()
# d42.get_all_buildings()
# d42.get_all_rooms()
# d42.post_building({'name':'Building2'})
# d42.post_device({'name':'db-080-westport','type':'cluster','in_service':'no','virtual_host':'yui','service_level':'production','macaddress':'aabbccedffff'})
d42.get_all_devices()
