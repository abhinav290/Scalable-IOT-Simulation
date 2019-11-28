
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
        if data < 50 or data > 100:
            return True
        return False


glucose_sensor = GlucoseSensor("3")
glucose_sensor.start()
