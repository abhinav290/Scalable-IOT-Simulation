import random
from iot.body2.sensors.sensor import Sensor


class LacticAcidSensor(Sensor):

    def sense(self):
        super().sense()
        lactic_acid = random.uniform(0,3)
        return {'lactic_acid': lactic_acid}

    def is_critical_data(self, data):
        if (data['lactic_acid'] < 0.5 or data['lactic_acid'] > 1):
            return True
        else:
            return False


lactic_acid_sensor = LacticAcidSensor("5")
lactic_acid_sensor.start()
