from datetime import datetime
import time


from iot.body1.sensors.sensor import Sensor
from iot.body1.sensors.device_config import Util

class Sink(Sensor):

    def get_config(self):
        self.config = Util.get_sink_config(self.id)

    def set_config(self):
        Util.set_sink_config(self.id, self.config)

    def receive_data(self):
        received_messages = Sensor.queueService.receive_and_delete_message(self.sinkQueueUrl)
        if received_messages:
            self.temp_data.append(self.process_data(received_messages))


    def process_data(self, data):
        return data
        # if 'Messages' in normal_response:
        #     messages = normal_response['Messages']
        #     for message in messages:
        #         body= message['Body']
        #         for key in body.keys():
        #             if key in self.final_data:
        #                 self.final_data[key].append(body[key])
        #             else:
        #                 self.append(body)
        # if 'Messages' in critical_response:
        #     messages = critical_response['Messages']
        #     for message in messages:
        #         body= message['Body']
        #         for key in body.keys():
        #             if key in self.final_data:
        #                 self.final_data[key].append(body[key])
        #             else:
        #                 self.append(body)


    # TODO add the code for sending data to sink.
    def send_to_edge(self):
        response = Sensor.queueService.send(self.config['edge_queue_url'], self.temp_data, str(self.id))
        print('Sending data - to edge :-- ' + str(self.temp_data))
        self.temp_data = []


    def start(self):
        run = 1
        while self.config['battery'] > 0:
            self.config['status'] = True
            self.set_config()
            start_time = datetime.now().timestamp()
            time.sleep(2)
            #print('Waking ' + str(datetime.now()))
            print('Battery level - ' + str(self.config['battery']))

            data = self.receive_data()
            self.send_to_edge()

            end_time = datetime.now().timestamp()
            active_time = float(end_time) - float(start_time)
            self.config['battery'] = self.config['battery'] - self.calculate_battery_loss(active_time, self.calculate_data_size('dfsfd'))
            if self.config['battery'] < 0:
                self.config['battery'] = 0
            self.set_config()
            self.config['status'] = False
            run += 1
            #print('Sleeping ' + str(datetime.now()))
            time.sleep(self.calculate_off_time(active_time))

sink=Sink("221")
sink.start()
