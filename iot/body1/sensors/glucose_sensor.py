
import random
import socket
import time
from iot.body1.sensors.sensor import Sensor


class GlucoseSensor(Sensor):

    def __init__(self, id):
        super().__init__(id)
        self.last_insulin_injection_time = None

    def sense(self):
        super().sense()
        return round(random.uniform(40, 120), 1)

    def is_critical_data(self, data):
        if data < 50:
            return True
        if data > 100:
            # and self.should_inject_insulin()
            s = self.instantiate_socket()
            message = "Critical data. Need to inject insulin."
            print(message)
            s.sendall(message.encode())
            self.turn_off_socket_connection(s)
            return True
        return False

    def should_inject_insulin(self):
        current_time = time.time()
        if self.last_insulin_injection_time is not None:
            print("Time diff bw last & now" +
                  str(self.last_insulin_injection_time - current_time))
            return self.last_insulin_injection_time - current_time > 10
        else:
            self.last_insulin_injection_time = current_time
            return True

    def instantiate_socket(self):
        host = '127.0.0.1'
        port = 5533
        s = socket.socket()
        s.connect((host, port))
        return s

    def turn_off_socket_connection(self, s):
        s.close()


glucose_sensor = GlucoseSensor("3")
glucose_sensor.start()
