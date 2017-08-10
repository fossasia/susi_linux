import time
import RPi.GPIO as GPIO

from .wake_button import WakeButton


class RaspberryPiWakeButton(WakeButton):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while True:
            input_state = GPIO.input(18)
            if not input_state:
                self.on_detected()
                time.sleep(0.2)
