from iot.utils.queue_service import AWSService
import ast
import json
import os


class Edge:
    queue_service = AWSService()

    def __init__(self):
        # Edge Queue URL
        self.edge_url = 'https://sqs.eu-west-1.amazonaws.com/386707910583/sink-to-edge.fifo'
        self.temp_data = {}
        self.filePath = 'data.json'

    def receive_data(self):
        received_messages = Edge.queue_service.receive_and_delete_message(self.edge_url)
        if received_messages:
            self.process_data(received_messages)

    def process_data(self, data):
        for val in data:
            device_dict = ast.literal_eval(val)
            for device_id in device_dict.keys():
                if str(device_id) not in self.temp_data:
                    self.temp_data[str(device_id)] = {}
                sensor_dict = device_dict[str(device_id)]
                for sensor_id in sensor_dict.keys():
                    if str(sensor_id) not in self.temp_data[str(device_id)]:
                        self.temp_data[str(device_id)][str(sensor_id)] = []
                    for reading in sensor_dict[str(sensor_id)]:
                        self.temp_data[str(device_id)][str(sensor_id)].append(reading)
        self.update_file()

    def update_file(self):
        data = {}
        if os.path.exists(self.filePath):
            f = open(self.filePath, 'r+')
            data = json.loads(f.read())
            f.close()

        for device_id in self.temp_data.keys():
            if str(device_id) not in data:
                data[str(device_id)] = {}
            for sensor_id in self.temp_data[str(device_id)].keys():
                if str(sensor_id) not in data[str(device_id)]:
                    data[str(device_id)][str(sensor_id)] = []
                for reading in self.temp_data[str(device_id)][str(sensor_id)]:
                    data[str(device_id)][str(sensor_id)].append(reading)
        json.dump(data, open(self.filePath, 'w+'))

    # TODO add the code for sending data to sink.
    def store_to_file(self):
        pass

    def start(self):
        while True:
            self.receive_data()


# Edge node for processing of normal data and creating a file which can be uploaded to S3.
edgeLaptop = Edge()
edgeLaptop.start()
