import random
from iot.body2.sensors.sensor import Sensor


class Accelerometer(Sensor):

    def sense(self):
        super().sense()
        force = random.uniform(-1, 1)
        return {'force': force}

    def is_critical_data(self, data):
        if (data['force'] < -0.5 or data['force'] > 0.5):
            return True
        else:
            return False


accelerometer = Accelerometer("4")
accelerometer.start()
