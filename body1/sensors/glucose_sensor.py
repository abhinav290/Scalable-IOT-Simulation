import random
from scalable.body1.sensors.sensor import Sensor


class GlucoseSensor(Sensor):

    def sense(self):
        super().sense()
        return round(random.uniform(40, 120), 1)

    def is_critical_data(self, data):
        if data < 50:
            return True
        if data>100:
            #inject insulin send a message to actuator.
            return True
        return False


temp_ear_sensor = GlucoseSensor("3")
temp_ear_sensor.start()
