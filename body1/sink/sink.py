from datetime import datetime
import json
import sys
import time

config_file = './../sensors/config.json'


def read_config():
    return json.loads(open(config_file, 'r').read())


class Sensor:
    id = ''
    config = {}
    temp_data = []

    def __init__(self, id):
        print('Creating sensor' + str(id))
        self.id = id
        self.get_config()

    def calculate_data_size(self, data):
        return sys.getsizeof(data)

    def calculate_off_time(self, active_time):
        return ((100 - self.config['duty_cycle']) / 100) * active_time

    def calculate_battery_loss(self, active_time, data_transmitted):
        return 1

    def get_config(self):
        self.config = read_config()[self.id]

    def set_config(self, ):
        json_data = read_config()
        json_data[self.id] = self.config
        with open(config_file, 'w') as json_file:
            json.dump(json_data, json_file)

    # TODO Measure data and see if it needs to be transmitted.
    # Method needs to be overridden.
    def sense(self):
        time.sleep(1)

    # TODO add the code for seeing the importance of data.
    # Method needs to be overridden
    def is_critical_data(self, data):
        pass

    # TODO add the code for sending data to sink.
    def send_to_sink(self, data):
        print('Sending data - ' + str(data))

    def send_to_forwarder(self, data):
        self.send_to_sink(data)

    def is_forwarder(self):
        if self.id == 1:
            return True
        return False

    def add_to_temp_data(self, data):
        self.temp_data.append(data)

    def process(self, run):
        print('Processing '+ str(run % self.config['transmission_cycle']))
        data = self.sense()
        if self.is_critical_data(data):
            data = {"type": "critical", "data": data, "timestamp": datetime.now().timestamp()}
            self.send_to_sink(data)
            return self.calculate_data_size(data)
        data = {"type": "normal", "data": data, "timestamp": datetime.now().timestamp()}
        self.add_to_temp_data(data)
        if run % self.config['transmission_cycle'] == 0:
            self.send_to_forwarder(self.temp_data)
            return self.calculate_data_size(data)
        return 0

    def start(self):
        run = 1
        while self.config['battery'] > 0:
            run += 1
            self.config['status'] = True
            self.set_config()
            start_time = datetime.now().timestamp()
            #print('Waking ' + str(datetime.now()))
            print('Battery level - ' + str(self.config['battery']))
            data_transmitted = self.process(run)
            end_time = datetime.now().timestamp()
            active_time = float(end_time) - float(start_time)
            self.config['battery'] = self.config['battery'] - self.calculate_battery_loss(active_time, data_transmitted)
            if self.config['battery'] < 0:
                self.config['battery'] = 0
            self.set_config()
            self.config['status'] = False

            #print('Sleeping ' + str(datetime.now()))
            time.sleep(self.calculate_off_time(active_time))