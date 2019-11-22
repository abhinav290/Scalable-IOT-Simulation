from threading import Lock

import json
import os

sensor_config_dir = "config"
device_config_file = './../../device_config.json'
forwarder_file = 'forwarder.json'


class Util:
    lock = Lock()
    lock1 = Lock()
    THRESHOLD_BATTERY = 60

    @staticmethod
    def calculate_power_distance(config):
        return config['distance_to_sink'] / config['battery']

    @staticmethod
    def get_path(sensor_id):
        return os.path.join(sensor_config_dir, str(sensor_id) + '.json')

    @staticmethod
    def get_sensor_config(sensor_id):
        path = Util.get_path(sensor_id)
        return json.loads(open(path, 'r').read())

    @staticmethod
    def get_sink_config(sensor_id):
        path = 'config.json'
        print(os.getcwd())
        return json.loads(open(path, 'r').read())
    @staticmethod
    def set_sink_config(sensor_id, config):
        path = 'config.json'
        with open(path, 'w') as json_file:
            json.dump(config, json_file)

    @staticmethod
    def set_sensor_config(sensor_id, config):
        path = path = Util.get_path(sensor_id)
        with open(path, 'w') as json_file:
            json.dump(config, json_file)

    @staticmethod
    def decide_forwarder():
        Util.lock.acquire()
        config = []
        forwarder = None
        for file in os.listdir(sensor_config_dir):
            sensor_config = Util.get_sensor_config(os.path.splitext(file)[0])
            if sensor_config['status'] and float(sensor_config['battery']) > Util.THRESHOLD_BATTERY:
                config.append({'id': os.path.splitext(file)[0],
                               'power_consumption': Util.calculate_power_distance(sensor_config)})
        config.sort(key=lambda i: (i['power_consumption']))
        if config:
            print(config)
            forwarder = config[0]
            json.dump(forwarder, open(forwarder_file, 'w'))
        Util.lock.release()
        return forwarder

    @staticmethod
    def read_forwarder():
        return json.loads(open(forwarder_file,'r').read())['id']

    @staticmethod
    def read_forwarder_config():
        return Util.get_sensor_config(Util.read_forwarder())