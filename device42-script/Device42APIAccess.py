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
        self.DEVICES_RACK_URL = config.get('credentials', 'DEVICES_RACK_URL')
        self.HARDWARE_MODEL = config.get('credentials', 'HARDWARE_MODEL')

    def get_all_buildings(self):
        """
        Getting all buildings information
        """
        try:
            response = requests.request('GET', self.BUILDINGS_URL, auth=(self.user, self.password), verify=False)
            # print response.text
            response.encoding = 'utf-8'
            output = response.json()
            return output
        except requests.exceptions.RequestException as err:
            print err

    def get_all_rooms(self):
        """
        Getting all rooms information from device42 application using get request
        """
        try:
            response = requests.get(self.ROOMS_URL, auth=(self.user, self.password), verify=False)
            print response.text
            response.encoding = 'utf-8'
            output = response.json()
            for value in output['rooms']:
                print value['name']
            return output
        except requests.exceptions.RequestException as err:
            print err

    def get_all_racks(self):
        """
        Getting all racks information from device42 application using get request
        """
        try:
            response = requests.get(self.RACKS_URL, auth=(self.user, self.password), verify=False)
            print response.text
            response.encoding = 'utf-8'
            output = response.json()
            return output
        except requests.exceptions.RequestException as err:
            print err

    def get_all_models(self):
        """
        Getting all racks information from device42 application using get request
        """
        try:
            response = requests.get(self.HARDWARE_MODEL, auth=(self.user, self.password), verify=False)
            print response.text
            response.encoding = 'utf-8'
            output = response.json()
            return output
        except requests.exceptions.RequestException as err:
            print err

    def get_all_devices(self):
        """
        Getting all devices information from device42 application using get request
        """
        try:
            response = requests.get(self.DEVICES_URL, auth=(self.user, self.password), verify=False)
            print response.text
            response.encoding = 'utf-8'
            res_json = response.json()
            return res_json
        except requests.exceptions.RequestException as err:
            print err

    def post_building(self, payload):
        """
        Create a building with given data in device42 using POST
        """
        try:
            print "building payload ",payload
            response = requests.post(self.BUILDINGS_URL, auth=(self.user, self.password), verify=False,
                                         data=payload)
            print response.text
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_room(self, payload):
        """
        Create a room with given data in device42 using POST
        """
        try:
            response = requests.post(self.ROOMS_URL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_rack(self, payload):
        """
        Create a room with given data in device42 using POST
        """
        try:
            response = requests.post(self.RACKS_URL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_hardware_model(self, payload):
        """
                Create a hardware model with given data in device42 using POST
        """
        try:
            print "hardware paylaod ",payload
            response = requests.post(self.HARDWARE_MODEL, auth=(self.user, self.password), verify=False, data=payload)
            print response.text
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_device_rack(self, payload):
        """
        Create a device with given data in device42 using POST
        """
        try:
            if 'hardware' in payload and payload['hardware'] != '' or payload['hardware'] is not None:
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hardware'])
                if not is_found:
                    res = self.post_hardware_model(payload['hardware'])
            if res.status_code !=200 and 'building' in payload and payload['building'] != '' or payload['building'] is not None:
                buildings = self.get_all_buildings()
                is_found = self.is_building_exists(buildings, payload['building'])
                if not is_found:
                    self.post_building(payload['building'])

                if 'room' in payload and payload['room'] != '' or payload['room'] is not None:
                    rooms = self.get_all_rooms()
                    is_found = self.is_room_exists(rooms, payload['room'])
                    if not is_found:
                        room_dict = dict((key, payload[key]) for key in ("room", "building"))
                        self.post_room(room_dict)

                if 'rack' in payload and payload['rack'] != '' or payload['rack'] is not None:
                    racks = self.get_all_racks()
                    is_found = self.is_rack_exists(racks, payload['rack'])
                    if not is_found:
                        rack_dict = dict((key, payload[key]) for key in ('building', 'room', 'rack'))
                        self.post_rack(rack_dict)

            response = requests.post(self.DEVICES_RACK_URL, auth=(self.user, self.password), verify=False, data=payload)
            return response
        except requests.exceptions.RequestException as err:
            print err

    def post_device(self, payload):
        try:
            if 'hardware' in payload and payload['hardware'] != '' or payload['hardware'] is not None:
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hardware'])
                if not is_found:
                    self.post_hardware_model(payload['hardware'])
            response = requests.post(self.DEVICES_URL, auth=(self.user, self.password), verify=False, data=payload)
            return response
        except requests.exceptions.RequestException as err:
            print err

    @staticmethod
    def is_building_exists(buildings, building_name):
        is_found = False
        for value in buildings['buildings']:
            if building_name == value['name']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_room_exists(rooms, room_name):
        is_found = False
        for value in rooms['rooms']:
            if room_name == value['name']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_rack_exists(racks, rack_name):
        is_found = False
        for value in racks['racks']:
            if rack_name == value['name']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_hardware_exists(hardware_models, model_name):
        is_found = False
        for value in hardware_models['models']:
            if model_name == value['name']:
                is_found = True
                break
        return is_found

    def post_buildings_csv(self, filename):

        """
            Read data from csv file and create a building in device42 using POST
        """
        if os.path.isfile(filename) and filename != '' and filename.endswith('.csv'):
            try:
                file_object = open(filename, 'r')
                records = csv.DictReader(file_object)

                for record in records:
                    try:
                        print record
                        response = self.post_building(record)
                        if response is not None:
                            print response.text
                    except requests.exceptions.RequestException as err:
                        print err

            except csv.Error as err:
                print err
        else:
            print "invalid file"

    def post_devices_csv(self, filename):
        """
         Read data from csv file and create a building in device42 using POST
        """
        if os.path.isfile(filename) and filename != '' and filename.endswith('.csv'):
            try:
                file_object = open(filename, 'r')
                records = csv.DictReader(file_object)

                for record in records:
                    try:
                        record = dict((k.lower(), v.lower()) for k, v in record.iteritems())
                        if 'building' or 'rack_id' in record and record['building'] or record['rack_id'] is not None:
                            print "entered if case building exists"
                            response = self.post_device_rack(record)
                        else:
                            response = self.post_device(record)
                        if response is not None:
                            print response.text
                    except requests.exceptions.RequestException as err:
                        print err
                    break
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
            response = requests.delete(self.BUILDINGS_URL + str(building_id), auth=(self.user, self.password),
                                       verify=False)
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
# d42.get_all_buildings()
#d42.get_all_rooms()
d42.post_devices_csv('deviceHard.csv')
# d42.post_building({'name':'Building2'})
# d42.post_device({'name':'db-080-westport','type':'cluster','in_service':'no','virtual_host':'yui','service_level':'production','macaddress':'aabbccedffff'})
# d42.get_all_devices()
# d42.delete_building(1)
# d42.post_buildings_csv('buildings.csv')
# d42.delete_device(3)
