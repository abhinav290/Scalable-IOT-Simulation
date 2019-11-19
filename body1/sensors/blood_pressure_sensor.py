from scalable.body1.sensors.sensor import Sensor
import random


class BloodPressureSensor(Sensor):

    def sense(self):
        super().sense()
        systolic = random.randint(70, 190)
        diastolic = random.randint(40, 100)
        return {'systolic': systolic, 'diastolic': diastolic}

    def is_critical_data(self, data):
        if (data['systolic'] < 90 and data['diastolic'] < 60) or \
                (data['systolic'] >= 140 or data['diastolic'] >= 90):
            return True
        return False


bp_sensor = BloodPressureSensor("1")
bp_sensor.start()
