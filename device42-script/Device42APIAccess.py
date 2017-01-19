import ConfigParser
import os
import sys
import csv
import logging
import datetime
import requests
from requests import RequestException
from requests import HTTPError
import ParameterException
import json

'''

'''


class Device42Svc:
    def __init__(self, filename):
        self.logger = self.config_logs()
        if len(sys.argv) > 1:
            cfg_filename = sys.argv[1]
            print cfg_filename
            if len(sys.argv) == 3:
                self.csv_filename = sys.argv[2]
            else:
                self.csv_filename = 'deviceHard.csv'
        if not filename == '':
            cfg_filename = filename
            print cfg_filename
            self.csv_filename = 'deviceHard.csv'

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
                if self.is_cache:
                    self.update_cache()

            except ConfigParser.Error as err:
                self.logger.error(err)
        else:
            self.logger.info("please provide config file name")

    def update_cache(self):
        path = os.getcwd()
        buildings_file_path = path + "/cache/buildings_cache.json"
        response = self.get_all_buildings()
        print response.json()
        if response.status_code == 200:
            if os.path.getsize(buildings_file_path) == 0:
                print "entered if"
                with open(buildings_file_path, 'w') as f:
                    json.dump(response.json(), f)
            else:
                output = response.json()
                with open(buildings_file_path, 'r') as f:
                    data = json.load(f)
                if output['total_count'] == data['total_count']:
                    self.logger.info("up to date")
        else:
            print "invalid response"

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

    def post_method(self, url, payload):
        """
        Generic method for post
        :return:
        """
        try:
            response = requests.post(url, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)
            raise

    def post_building(self, payload):
        """
        Create a building with given data in device42 using POST
        """
        try:
            self.check_params('building', payload)
        except ParameterException.ParameterException as err:
            self.logger.error(err)
        response = self.post_method(self.buildings_url, payload)
        return response

    def post_room(self, payload):
        """
        Create a room with given data in device42 using POST
        """
        try:
            self.check_params('room', payload)
            if 'building' in payload and payload['building'] != '' or payload['building'] is not None:
                buildings = self.get_all_buildings()
                is_found = self.is_building_exists(buildings, payload['building'])
                if not is_found:
                    building_dict = {'name': payload['building']}
                    self.post_building(building_dict)
            response = self.post_method(self.rooms_url, payload)
            return response
        except (requests.exceptions.RequestException, ParameterException.ParameterException) as err:
            self.logger.error(err)
            raise err

    def post_rack(self, payload):
        """
        Create a rack with given data in device42 using POST
        """
        try:
            self.check_params('rack', payload)
            if 'room' in payload and (payload['room'] != '' or payload['room'] is not None):
                rooms = self.get_all_rooms()
                room_dict = {'name': payload['room'], 'building': payload['building']}
                is_found = self.is_room_exists(rooms, room_dict)
                if not is_found:
                    self.post_room(room_dict)
            if 'size' not in payload:
                payload['size'] = 42
            response = requests.post(self.racks_url, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)
            raise

    def post_hardware_model(self, payload):
        """
                Create a hardware model with given data in device42 using POST
        """
        try:
            response = requests.post(self.hardware_model, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)
            raise

    def post_device_rack(self, payload):
        """
        Create a device with given data in device42 using POST
        """
        try:
            if 'hw_model' in payload and \
                    (payload['hw_model'] != '' and payload['hw_model'] is not None):
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hw_model'])
                if not is_found:
                    hardware_dict = {'name': payload['hw_model']}
                    self.post_hardware_model(hardware_dict)

            if 'rack' in payload and payload['rack'] != '' or payload['rack'] is not None:
                racks = self.get_all_racks()
                rack_dict = {'name': payload['rack'], 'room': payload['room'],
                             'building': payload['building']}
                is_found = self.is_rack_exists(racks, rack_dict)
                if not is_found:
                    self.post_rack(rack_dict)
            if 'start_at' not in payload:
                payload['start_at'] = 'auto'

            response = requests.post(self.devices_rack_url, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

    def post_device(self, payload):
        """
        Creates a device with given data in Device42 using POST
        :param payload:
        :return:
        """
        try:
            self.check_params('device', payload)
            if 'hardware' in payload and (payload['hardware'] != ''
                                          and payload['hardware'] is not None):
                models = self.get_all_models()
                is_found = self.is_hardware_exists(models, payload['hardware'])
                if not is_found:
                    hardware_dict = {'name': payload['hardware']}
                    self.post_hardware_model(hardware_dict)
            response = requests.post(self.devices_url, auth=(self.user, self.password),
                                     verify=False, data=payload)
            self.logger.info(response)
            return response
        except requests.exceptions.RequestException as err:
            self.logger.error(err)

    def check_params(self, type_of_payload, payload):
        msg = "Success"
        if type_of_payload is 'building':
            if not payload['name']:
                msg = "missing required parameter building name"
        if type_of_payload is 'room':
            if not payload['name'] and (payload['building_id'] or payload['building']):
                msg = "missing required parameters room name, building or building_id"
        if type_of_payload is 'rack' or 'device':
            if not payload['name']:
                msg = "missing required parameters " + type_of_payload + " name"
        if not msg == "Success":
            self.logger.info(msg)
            raise ParameterException.ParameterException(msg)

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
                        response = self.post_building(record)
                        self.logger.info(response)
                    except requests.exceptions.RequestException as err:
                        self.logger.error(err)

            except csv.Error as err:
                self.logger.error(err)
        else:
            print "invalid file"

    def post_devices_csv(self):
        """
         Read data from csv file and create a building in device42 using POST
        """
        if os.path.isfile(self.csv_filename) and self.csv_filename != '' and self.csv_filename.endswith('.csv'):
            try:
                file_object = open(self.csv_filename, 'r')
                records = csv.DictReader(file_object)

                for record in records:
                    try:
                        record = dict((k.lower(), v) for k, v in record.iteritems())
                        if 'building' or 'rack_id' in record and \
                                record['building'] or record['rack_id'] is not None:
                            response = self.post_device_rack(record)
                            self.logger.info(response)
                        else:
                            response = self.post_device(record)
                            self.logger.info(response)
                    except requests.exceptions.RequestException as err:
                        print err
            except csv.Error as err:
                self.logger.error(err)
        else:
            print "invalid file"

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


d42 = Device42Svc('credentials.cfg')
d42.get_all_buildings()
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
