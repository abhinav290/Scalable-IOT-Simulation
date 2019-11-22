'''
    Device: Acutator
    Agenda: Communicates with glucose_sensor
    Desc: Uses socket to communicate with glucose sensor. Sleeps for relatively longer duration.
'''

from datetime import datetime
import socket
import os


class Actuator():

    def create_config(self):
        return {
            "battery": 100.0,
            "insulin_left": 500.0
        }

    def __init__(self):
        os.system("kill $(lsof -ti:5533)")  # Frees up the required port
        self.config = self.create_config()
        self.sck = socket.socket()
        self.sck.bind(('127.0.0.1', 5533))
        self.sck.listen(1)
        cSck, address = self.sck.accept()
        while True:
            msg = cSck.recv(1024).decode('utf-8')
            if msg is not None:
                print(msg)
                self.inject_insulin()

    def inject_insulin(self):
        print("Injecting insulin...")
        start_time = datetime.now().timestamp()
        end_time = datetime.now().timestamp()
        active_time = self.get_active_time(start_time=start_time, end_time=end_time)
        self.calculate_off_time(active_time)
        battery_lost = self.calculate_battery_loss(active_time, True)
        self.update_battery(battery_lost)
        self.update_insulin_level(self)
        print("Power left: " + str(self.config["battery"]))
        print("Insulin left: " + str(self.config["insulin_left"]))
        if self.config["insulin_left"] < 50:
            print("Insulin level critical. Refilling")
            self.refill_actuator()

    def refill_actuator(self):
        self.config["insulin_left"] = 500

    def update_battery(self, battery_lost):
        self.config["battery"] = float(self.config["battery"]) - battery_lost

    def update_insulin_level(self, insulin_injected=10):
        # self.config["insulin_left"] = float(
        #     self.config["insulin_left"]) - insulin_injected
        pass

    def get_active_time(self, start_time=0, end_time=0):
        return float(end_time) - float(start_time)

    def calculate_off_time(self, active_time):
        return 10

    def calculate_battery_loss(self, active_time, was_injection_involved=False):
        TRANSMISSION_battery, INJECTION_battery, INJECTION_TIME = 0.01, 0.1, 0.2
        transmission_time = (active_time + INJECTION_TIME) if was_injection_involved else active_time
        return ((transmission_time * TRANSMISSION_battery) + (
                    INJECTION_TIME * INJECTION_battery)) if was_injection_involved else (
                    transmission_time * TRANSMISSION_battery)


if __name__ == "__main__":
    a = Actuator()
# To free port kill $(lsof -ti:3000)
