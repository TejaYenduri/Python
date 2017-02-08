import ConfigParser
import os
import csv
import logging
import datetime
import requests
from requests import RequestException
from requests import HTTPError
from ParameterException import ParameterException
import json

'''

'''


class Device42Svc:
    def __init__(self, filename):

        cfg_filename = filename
        self.logger = self.config_logs()
        if cfg_filename != '' and os.path.isfile(cfg_filename) and cfg_filename.endswith('.cfg'):
            try:
                config = ConfigParser.SafeConfigParser()
                config.read(cfg_filename)
                self.user = config.get('credentials', 'USER')
                self.password = config.get('credentials', 'PASSWORD')
                self.base_url = config.get('credentials', 'BASE_URL')
                self.buildings_url = config.get('credentials', 'BUILDINGS_URL')
                self.rooms_url = config.get('credentials', 'ROOMS_URL')
                self.racks_url = config.get('credentials', 'RACKS_URL')
                self.devices_url = config.get('credentials', 'DEVICES_URL')
                self.devices_rack_url = config.get('credentials', 'DEVICES_RACK_URL')
                self.hardware_model = config.get('credentials', 'HARDWARE_MODEL')
                self.is_cache = config.get('credentials', 'IS_CACHE')
                self.buildings_cache = config.get('credentials', 'BUILDINGS_CACHE')
                self.rooms_cache = config.get('credentials', 'ROOMS_CACHE')
                self.racks_cache = config.get('credentials', 'RACKS_CACHE')
                self.hardware_cache = config.get('credentials', 'HARDWARE_CACHE')
                self.devices_cache = config.get('credentials', 'DEVICES_CACHE')
                self.update_cache(self.buildings_cache, self.buildings_url, "buildings")
                self.update_cache(self.racks_cache, self.racks_url, "racks")
                self.update_cache(self.hardware_cache, self.hardware_model, "models")
                self.update_cache(self.rooms_cache, self.rooms_url, "rooms")
                self.update_cache(self.devices_cache, self.devices_url, "Devices")

            except ConfigParser.Error as err:
                self.logger.error(err)
        else:
            self.logger.info("please provide config file name")

    def update_cache(self, file_path, url, type_of):
        try:
            path = os.getcwd() + file_path
            response = self.get_method(url)
            if response is not None and response.status_code == 200:
                response.encoding = 'utf-8'
                output = response.json()
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    cache_data = self.read_from_cache(path)
                    if cache_data == output[type_of]:
                        self.logger.info("cache up to date")
                    else:
                        records_list = output[type_of]
                        records = [a for a in records_list if (a not in cache_data)]
                        for record in records:
                            cache_data.append(record)
                        with open(path, "w") as file_object:
                            json.dump(cache_data, file_object, indent=4, sort_keys=True)
                        self.logger.info("updated cache")
                else:
                    with open(path, 'w') as f:
                        json.dump(output[type_of], f, indent=4, sort_keys=True, ensure_ascii=False)
                        self.logger.info("created and updated cache")
            else:
                self.logger.info(response)
        except (OSError, RequestException, HTTPError) as err:
            self.logger.info(err)

    @staticmethod
    def read_from_cache(file_path):
        with open(file_path, 'r') as f:
            response = json.load(f)
        return response

    @staticmethod
    def write_to_cache(file_path, data):
        response = Device42Svc.read_from_cache(file_path)
        response.append(data)
        with open(file_path, "w") as file_object:
            json.dump(response, file_object, indent=4, sort_keys=True)

    @staticmethod
    def config_logs():
        """
        logging configuration
        :return:
        """
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        log_name = str(datetime.date.today()) + '.log'
        # create a file handler
        handler = logging.FileHandler(log_name)
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_method(self, url):
        """
        Generic method for get request
        :param url:
        :return:
        """
        try:
            response = requests.request('GET', url,
                                        auth=(self.user, self.password), verify=False)
            response.encoding = 'utf-8'
            self.logger.info(response)
            return response
        except (RequestException, HTTPError) as err:
            self.logger.error(err)

    def get_all_buildings(self):
        """
        Getting all buildings information
        """
        response = self.get_method(self.buildings_url)
        return response

    def get_all_rooms(self):
        """
        Getting all rooms information from device42 application using get request
        """
        response = self.get_method(self.rooms_url)
        return response

    def get_all_racks(self):
        """
        Getting all racks information from device42 application using get request
        """
        response = self.get_method(self.racks_url)
        return response

    def get_all_models(self):
        """
        Getting all hardware models information from device42 application using get request
        """
        response = self.get_method(self.hardware_model)
        return response

    def get_all_devices(self):
        """
        Getting all devices information from device42 application using get request
        """
        response = self.get_method(self.devices_url)
        return response

    def post_method(self, url, payload, file_path):
        """
        Generic method for post
        :return:
        """
        try:
            response = requests.post(url, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            if response.status_code == 200:
                self.write_to_cache(file_path, payload)
                
            return response
        except RequestException as err:
            self.logger.error(err)

    def post_building(self, payload):
        """
        Create a building with given data in device42 using POST
        """
        try:
            self.check_params(payload, {'name'})
        except ParameterException as err:
            self.logger.error(err)
        response = self.post_method(self.buildings_url, payload, os.getcwd() + self.buildings_cache)
        return response

    def post_room(self, payload):
        """
        Create a room with given data in device42 using POST
        """
        try:

            building_response = None
            response = None
            is_found = False
            if 'building' in payload:
                self.check_params(payload, {'name', 'building'})
                buildings = self.get_all_buildings()
                if buildings is not None:
                    is_found = self.is_building_exists(buildings.json(), payload['building'])
                if not is_found:
                    building_dict = {'name': payload['building']}
                    building_response = self.post_building(building_dict)
                    if building_response.status_code == 200:
                        response = self.post_method(self.rooms_url, payload, os.getcwd() + self.rooms_cache)
                else:
                    response = self.post_method(self.rooms_url, payload, os.getcwd() + self.rooms_cache)
            else:
                self.check_params(payload, {'name', 'building_id'})
                response = self.post_method(self.rooms_url, payload, os.getcwd() + self.rooms_cache)
            if response.status_code == 200:
                return response
            else:
                if building_response is not None and building_response.status_code == 200:
                    building_id = building_response.json()["msg"][1]
                    self.delete_method_using_id(self.buildings_url, building_id)

        except (RequestException, HTTPError, ParameterException) as err:
            self.logger.error(err)
            raise err

    def post_rack(self, payload):
        """
        Create a rack with given data in device42 using POST
        """
        try:
            is_found = False
            response = None
            if 'size' not in payload:
                payload['size'] = 42
            if 'building' in payload:
                self.check_params(payload, {'room', 'building', 'name', 'size'})
                rooms = self.get_all_rooms()
                room_dict = {'name': payload['room'], 'building': payload['building']}
                is_found = self.is_room_exists(rooms, room_dict)
                if not is_found:
                    room_response = self.post_room(room_dict)
                    if room_response.status_code == 200:
                        response = self.post_method(self.racks_url, payload, os.getcwd() + self.rooms_cache)
                        if response.status_code == 200:
                            return response
                        else:
                            room_id = room_response.json()["msg"][1]
                            self.logger.info(room_id)
                            self.delete_method_using_id(self.rooms_url, room_id)
                            if self.is_cache == 'False':
                                building_id = self.get_id(payload['building'], self.buildings_url, "buildings",
                                                          "building_id")
                                self.delete_method_using_id(self.buildings_url, building_id)

            self.check_params(payload, {'name', 'size'})
            response = self.post_method(self.racks_url, payload, os.getcwd() + self.racks_cache)
            self.logger.info(response)
            if response.status_code == 200:
                return response
        except (RequestException, HTTPError, ParameterException) as err:
            self.logger.error(err)

    def post_hardware_model(self, payload):
        """
                Create a hardware model with given data in device42 using POST
        """
        try:
            self.check_params(payload, {'name'})
            response = self.post_method(self.hardware_model, payload, os.getcwd() + self.hardware_cache)
            self.logger.info(response)
            return response
        except (RequestException, ParameterException) as err:
            self.logger.error(err)
            raise

    def post_device_rack(self, payload):
        """
        Create a device with given data in device42 using POST
        """
        try:
            if 'hw_model' in payload:
                self.check_params(payload, {'hw_model'})
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hw_model'])
                if not is_found:
                    hardware_dict = {'name': payload['hw_model']}
                    self.post_hardware_model(hardware_dict)
            if 'start_at' not in payload:
                payload['start_at'] = 'auto'
            is_found = False
            if 'building' in payload:
                self.check_params(payload, {'device', 'room', 'building', 'start_at'})
                racks = self.get_all_racks()
                rack_dict = {'name': payload['rack'], 'room': payload['room'],
                             'building': payload['building']}
                is_found = self.is_rack_exists(racks, rack_dict)
            if is_found or 'rack_id' in payload:
                self.check_params(payload, {'device', 'rack_id', 'start_at'})
                response = self.post_method(self.devices_rack_url, payload, os.getcwd() + self.devices_cache)
                self.logger.info(response)
                return response
            if not is_found:
                rack_response = self.post_rack(rack_dict)
                if rack_response.status_code == 200:
                    response = self.post_method(self.devices_rack_url, payload, os.getcwd() + self.devices_cache)
                    if response.status_code == 200:
                        return response
                    else:
                        self.delete_method_using_id(self.racks_url, rack_response.json()["msg"][1])
        except RequestException as err:
            self.logger.error(err)

    def post_device(self, payload):
        """
        Creates a device with given data in Device42 using POST
        :param payload:
        :return:
        """
        try:
            self.check_params(payload, {'name'})
            if 'hardware' in payload:
                self.check_params(payload, {'hardware'})
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hardware'])
                if not is_found:
                    hardware_dict = {'name': payload['hardware']}
                    self.post_hardware_model(hardware_dict)
            response = self.post_method(self.devices_url, payload, os.getcwd() + self.devices_cache)
            self.logger.info(response)
            return response
        except (RequestException, ParameterException) as err:
            self.logger.error(err)

    def check_params(self, payload, required_params):
        msg = "Success"
        if not all(key in payload and (payload[key] not in [None, '']) for key in required_params):
            msg = "missing required parameters " + str(required_params)
        if not msg == "Success":
            self.logger.info(msg)
            raise ParameterException(msg)

    @staticmethod
    def is_building_exists(buildings, building_name):
        """
        Checks whether building exists or not and returns truth value
        :param buildings:
        :param building_name:
        :return:
        """
        is_found = False
        for value in buildings['buildings']:
            if building_name == value['name']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_room_exists(rooms, room_dict):
        """
        Checks whether a room exists in the given building with the given name
        :param rooms:
        :param room_dict:
        :return:
        """
        is_found = False
        for value in rooms['rooms']:
            if room_dict['name'] == value['name'] and room_dict['building'] == value['building']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_rack_exists(racks, rack_dict):
        """
        Checks whether a rack exists with given name in the given room and building
        :param racks:
        :param rack_dict:
        :return:
        """
        is_found = False
        for value in racks['racks']:
            if rack_dict['name'] == value['name'] and rack_dict['room'] == value['room'] \
                    and rack_dict['building'] == value['building']:
                is_found = True
                break
        return is_found

    @staticmethod
    def is_hardware_exists(hardware_models, model_name):
        """
        Checks whether given hardware model exists or not and returns truth value
        :param hardware_models:
        :param model_name:
        :return:
        """
        is_found = False
        for value in hardware_models['models']:
            if model_name == value['name']:
                is_found = True
                break
        return is_found

    def get_id(self, name, url, type_of, id_type):
        response = self.get_method(url)
        if response.status_code == 200:
            output = response.json()
            for i in xrange(len(output[type_of])):
                if output[type_of]['name'] == name:
                    return output[type_of][id_type]
        return -1

    def post_buildings_csv(self, filename):

        """
            Read data from csv file and create a building in device42 using POST
        """
        if os.path.isfile(filename) and filename != '' and filename.endswith('.csv'):
            try:
                with open(filename) as file_handler:
                    keys_string = file_handler.readline()
                    keys = []
                    record = {}
                    if keys_string:
                        keys_string = keys_string.lower()
                        keys = keys_string.split(',')

                    for line in self.read_from_csv(file_handler):
                        values = line.split(',')
                        record = dict(zip(keys, values))
                    try:
                        response = self.post_building(record)
                        self.logger.info(response)
                    except requests.exceptions.RequestException as err:
                        self.logger.error(err)

            except csv.Error as err:
                self.logger.error(err)
        else:
            print "invalid file"

    @staticmethod
    def read_from_csv(file_object):
        while True:
            data = file_object.readline()
            if not data:
                break
            yield data

    def post_devices_csv(self, filename=None):
        """
         Read data from csv file and create a building in device42 using POST
        """
        if os.path.isfile(filename) and filename != '' and filename.endswith('.csv'):
            print filename
            success = False
            try:
                with open(filename) as file_handler:
                    keys_string = file_handler.readline()
                    count = 0
                    keys = []
                    if keys_string:
                        keys_string = keys_string.lower()
                        keys = keys_string.split(',')

                    for line in self.read_from_csv(file_handler):
                        values = line.split(',')
                        record = dict(zip(keys, values))
                        try:
                            if 'building' or 'rack_id' in record and \
                                    record['building'] or record['rack_id'] is not None:
                                response = self.post_device_rack(record)
                                self.logger.info(response)
                            else:
                                response = self.post_device(record)
                                self.logger.info(response)
                            if response is not None and response.status_code == 200:
                                count += 1
                            else:
                                self.logger.info(str(record) + " not inserted")
                        except (RequestException, ParameterException) as err:
                            self.logger.info(err)
                    if count >= 1:
                        success = True
                return success
            except (IOError, OSError) as err:
                self.logger.error(err)
        else:
            self.logger.info("invalid file. upload .csv file")

    def delete_method_using_id(self, url, entity_id):
        try:
            response = requests.delete(url + str(entity_id), auth=(self.user, self.password),
                                       verify=False)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

    def delete_building(self, building_id):
        """
             Delete building in device42
             Need to implement logic for removing racks and rooms and updating devices.
        """
        response = self.delete_method_using_id(self.buildings_url, building_id)
        return response

    def delete_device(self, device_id):
        """
         Delete building in device42
        """
        response = self.delete_method_using_id(self.devices_url, device_id)
        return response

# d42 = Device42Svc('credentials.cfg')
# d42.get_all_buildings()
# d42.get_all_rooms()
# d42.post_hardware_model({'name': 'PE 1950', 'type': '1', 'size': '1', 'depth': '1', 'part_no': '123', 'watts': '265',
#                        'spec_url': 'www.dell.com', 'manufacturer': 'dell', 'notes': 'hellp'})
# d42.post_hardware_model({'name': 'h1'})
# d42.post_devices_csv()
# d42.post_building({'name':'Building2'})
# d42.post_device({'name':'db-080-westport','type':'cluster','in_service':'no','virtual_host':'yui','service_level':'production','macaddress':'aabbccedffff'})
# d42.get_all_devices()
# d42.delete_building(1)
# d42.post_buildings_csv('buildings.csv')
# d42.delete_device(3)
# d42.post_device_rack(
#    {'device': 'nh-switch-01', 'building': 'New Haven DC', 'room': '1st floor', 'rack': 'RA1', 'start_at': '2',
#    'orientation': 'back'})
# d42.post_device({'name': 'TestDevice', 'serial_no': 'Ab123asd', 'in_service': 'yes', 'type': 'physical',
#                 'hardware': 'Generic Hardware 1U', 'service_level': 'production', 'os': 'RHEL Server', 'osver': '6.5',
#                 'memory': '16.000',
#                'cpucount': '80', 'cpucore': '8', 'notes': 'my special device'})
