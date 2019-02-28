import time
import logging
import RPi.GPIO as GPIO

from .wake_button import WakeButton


logger = logging.getLogger(__name__)


class RaspberryPiWakeButton(WakeButton):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while True:
            is_input = GPIO.input(17)
            if is_input:
                time.sleep(0.2)
                continue
            # Button pressed
            logger.debug('WakeButton is pressed')
            self.on_detected()
            time.sleep(0.2)
