from datetime import datetime

from iot.utils.queue_service import QueueService
from iot.body1.sensors.device_config import Util

import sys
import time


class Sensor:
    forwarderQueueUrl='https://sqs.eu-west-1.amazonaws.com/386707910583/Device1-sensor-to-forwarder.fifo'
    sinkQueueUrl='https://sqs.eu-west-1.amazonaws.com/386707910583/Device1-SensorToSink.fifo'
    queueService=QueueService()


    def set_forwarder(self, id):
        self.forwarder= id


    def __init__(self, id):
        print('Creating sensor' + str(id))
        self.id = id
        self.temp_data=[]
        self.get_config()

    def calculate_data_size(self, data):
        return sys.getsizeof(data)

    def calculate_off_time(self, active_time):
        return ((100 - self.config['duty_cycle']) / 100) * active_time

    def calculate_battery_loss(self, active_time, data_transmitted):
        transmission_time = data_transmitted/self.config['data_rate']
        return (active_time * self.config['active_power']) + (transmission_time * self.config['transmission_power'])

    def get_config(self):
        self.config = Util.get_sensor_config(self.id)

    def set_config(self):
        Util.set_sensor_config(self.id, self.config)

    # Method needs to be overridden.
    def sense(self):
        time.sleep(1)
        pass

    # Method needs to be overridden
    def is_critical_data(self, data):
        pass

    def send_to_sink(self, data):
        print('Sending data - ' + self.id + ' == ' + str(data))
        Sensor.queueService.send(Sensor.sinkQueueUrl, data, str(self.id))

    def send_to_forwarder(self, data):
        if self.is_forwarder():
            self.send_to_sink(self.get_payload(data))
            return
        print('Sending data to forwarder - '+ self.id + ' == '+ str(data))
        Sensor.queueService.send(Sensor.forwarderQueueUrl,self.get_payload(data), str(self.id))
        self.temp_data=[]

    def is_forwarder(self):
        print('Forwarder id' + str(self.forwarder))

        if self.forwarder == self.id:
            return True
        return False

    def add_to_temp_data(self, data):
        self.temp_data.append(data)

    def get_payload(self,data):
        return {str(self.id): data}

    def decide_forwarder(self):
        if self.is_forwarder() and self.config['battery'] < Util.THRESHOLD_BATTERY:
            Util.decide_forwarder()


    def receive_forwarder(self):
        data_transmitted = 0
        if self.is_forwarder():
            print('Forwarder node ' + self.id + ' trying to receive')
            data = Sensor.queueService.receive_and_delete_message(Sensor.forwarderQueueUrl)
            if data:
                print('Receiving data - ' + self.id + ' == ' + str(data))
                self.send_to_sink(data)
                data_transmitted += self.calculate_data_size(data)
        return data_transmitted

    def process(self, run):
        data=self.sense()
        if self.is_critical_data(data):
            data = self.get_payload(data=[{"type": "critical", "data": data, "timestamp": datetime.now().timestamp()}])
            # self.send_to_sink(data)
            return self.calculate_data_size(data)
        data = {"type": "normal", "data": data, "timestamp": datetime.now().timestamp()}
        self.add_to_temp_data(data)

        if run % self.config['transmission_cycle'] == 0:
            self.send_to_forwarder(self.get_payload(self.temp_data))
            return self.calculate_data_size(self.get_payload(self.temp_data))
        return 0

    def start(self):
        Util.decide_forwarder()
        run = 1
        while self.config['battery'] > 0:
            self.set_forwarder(Util.read_forwarder())
            self.config['status'] = True
            self.set_config()
            start_time = datetime.now().timestamp()
            data_transmitted = self.process(run)
            # Works for forwarder
            data_transmitted += self.receive_forwarder()
            end_time = datetime.now().timestamp()
            active_time = float(end_time) - float(start_time)
            self.config['battery'] = self.config['battery'] - self.calculate_battery_loss(active_time, data_transmitted)
            if self.config['battery'] < 0:
                self.config['battery'] = 0
            self.set_config()
            self.config['status'] = False
            self.decide_forwarder()
            run += 1
            time.sleep(self.calculate_off_time(active_time))