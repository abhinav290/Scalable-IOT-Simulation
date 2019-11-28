from datetime import datetime
import time
import ast

from iot.body1.sensors.sensor import Sensor
from iot.body1.sensors.device_config import Util

class Sink(Sensor):
    edge_queue_url = 'https://sqs.eu-west-1.amazonaws.com/386707910583/sink-to-edge.fifo'
    edge_critical_url = 'https://sqs.eu-west-1.amazonaws.com/386707910583/crirical-edge.fifo'

    def get_config(self):
        self.config = Util.get_sink_config(self.id)
        self.reading_map = {}

    def set_config(self):
        Util.set_sink_config(self.id, self.config)

    def receive_data(self):
        received_messages = Sensor.queueService.receive_and_delete_message(self.sinkQueueUrl)
        if received_messages:
            self.process_data(received_messages)

    def process_data(self, data):
        for val in data:
            print(val)
            try:
                sensor_dict = ast.literal_eval(val)
                print(sensor_dict.keys())
                for key in sensor_dict.keys():
                    if str(key) not in self.reading_map:
                        self.reading_map[str(key)] = []
                    for reading in sensor_dict[str(key)]:
                        if reading['type'] == 'critical':
                            self.alert_edge(str(key) + ' sensor is in critical situation ' + str(reading['data']))
                        self.reading_map[str(key)].append(reading)
            except:
                continue


    def alert_edge(self, data):
        print("Critical data" + data)
        Sensor.queueService.send(self.edge_critical_url, str({self.id: data}), str(self.id))


    def send_to_edge_aggregator(self):
        if self.reading_map:
            response = Sensor.queueService.send(self.edge_queue_url, str({self.id: self.reading_map}), str(self.id))
            print('Sending data - to edge :-- ' + str(self.reading_map))
            self.reading_map = {}


    def start(self):
        run = 1
        while self.config['battery'] > 0:
            self.config['status'] = True
            self.set_config()
            start_time = datetime.now().timestamp()
            time.sleep(2)
            print('Battery level - ' + str(self.config['battery']))

            data = self.receive_data()
            self.send_to_edge_aggregator()

            end_time = datetime.now().timestamp()
            active_time = float(end_time) - float(start_time)
            self.config['battery'] = self.config['battery'] - self.calculate_battery_loss(active_time, self.calculate_data_size('dfsfd'))
            if self.config['battery'] < 0:
                self.config['battery'] = 0
            self.set_config()
            self.config['status'] = False
            run += 1
            time.sleep(self.calculate_off_time(active_time))


# Sink id - can be any number.
sink = Sink("221")
sink.start()
