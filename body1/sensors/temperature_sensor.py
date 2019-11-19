import random
from scalable.body1.sensors.sensor import Sensor


class TemperatureSensorEar(Sensor):

    def sense(self):
        super().sense()
        return round(random.uniform(95.0, 105.0), 1)

    def is_critical_data(self, data):
        if data < 96.6 or data > 99.7:
            return True
        return False


temp_ear_sensor = TemperatureSensorEar("2")
temp_ear_sensor.start()
