import ConfigParser
import requests
import csv
import os

"""

"""


class Device42Svc:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read('credentials.cfg')
        self.user = config.get('credentials', 'USER')
        self.password = config.get('credentials', 'PASSWORD')
        self.BASE_URL = config.get('credentials', 'BASE_URL')
        self.BUILDINGS_URL = config.get('credentials', 'BUILDINGS_URL')
        self.ROOMS_URL = config.get('credentials', 'ROOMS_URL')
        self.RACKS_URL = config.get('credentials', 'RACKS_URL')
        self.DEVICES_URL = config.get('credentials', 'DEVICES_URL')

    def get_all_buildings(self):
        """
        Getting all buildings information
        """
        try:
            response = requests.request('GET', self.BUILDINGS_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def get_all_rooms(self):
        """
        Getting all rooms information from device42 application using get request
        """
        try:
            response = requests.get(self.ROOMS_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def get_all_devices(self):
        """
        Getting all devices information from device42 application using get request
        """
        try:
            response = requests.get(self.DEVICES_URL, auth=(self.user, self.password), verify=False)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def post_building(self, payload):
        """
        Create a building with given data in device42 using POST
        """
        try:
            if bool(payload) and 'name' in payload:
                response = requests.post(self.BUILDINGS_URL, auth=(self.user, self.password), verify=False,
                                         data=payload)
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
            response = requests.post(self.ROOMS_URL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
        except requests.exceptions.RequestException as err:
            print err

    def post_device(self, payload):
        """
        Create a device with given data in device42 using POST
        """
        try:
            response = requests.post(self.DEVICES_URL, auth=(self.user, self.password), verify=False, data=payload)
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_buildings_csv(self, filename):
        """
        Read data from csv file and create a device in device42 using POST
        """
        if os.path.isfile(filename) and filename != '' and filename.endswith('.csv'):
            try:
                file_object = open(filename, 'r')
                records = csv.DictReader(file_object)
                
                for record in records:
                    try:
                        print record
                        response = self.post_building(record)
                        if response != None:
                            print response.text                
                    except requests.exceptions.RequestException as err:
                        print err
                print "successfully created "+str(post_count)+" records in device42"
            except csv.Error as err:
                print err
        else:
            print "invalid file"

    def delete_building(self, building_id):
        """
               Delete building in device42
               Need to implement logic for removing racks and rooms and updating devices.
        """
        try:
            response = requests.delete(self.BUILDINGS_URL + str(building_id), auth=(self.user, self.password), verify=False)
            print response.url
            print response.text
        except requests.exceptions.RequestException as err:
            print err
    def delete_device(self, device_id):
        """
               Delete building in device42
        """
        try:
            response = requests.delete(self.DEVICES_URL + str(device_id), auth=(self.user, self.password), verify=False)
            print response.url
            print response.text
        except requests.exceptions.RequestException as err:
            print err


d42 = Device42Svc()
#d42.get_all_buildings()
# d42.get_all_rooms()
#d42.post_building({'name':'Building2'})
# d42.post_device({'name':'db-080-westport','type':'cluster','in_service':'no','virtual_host':'yui','service_level':'production','macaddress':'aabbccedffff'})
#d42.get_all_devices()
#d42.delete_building(1)
d42.post_buildings_csv('buildings.csv')
#d42.delete_device(3)