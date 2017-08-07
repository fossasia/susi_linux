from queue import Queue

import RPi.GPIO as GPIO
import time
from .wake_button import WakeButton


class RaspberryPiWakeButton(WakeButton):
    def __init__(self, detection_callback, callback_queue: Queue):
        super().__init__(detection_callback, callback_queue)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while True:
            input_state = GPIO.input(18)
            if not input_state:
                self.on_detected()
                self.is_active = False
                time.sleep(0.2)
