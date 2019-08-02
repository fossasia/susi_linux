import RPi.GPIO as GPIO
import time

from .scheduler import Schedule

class ActionScheduler(Schedule):

 def __init__(self):
    super().__init__()
    for i in range(20):
        time.sleep(1)
        print("sleeping....")
    self.button_detected

 def button_detected(channel, foo):
    super().on_detected()

 def run(self):
    pass
