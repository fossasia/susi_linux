import RPi.GPIO as GPIO
from .wake_button import WakeButton


class RaspberryPiWakeButton(WakeButton):

    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            17, GPIO.FALLING, 
            callback=self.button_detected, 
            bouncetime=300)

    def button_detected(channel, foo):
        super().on_detected()

    def run(self):
        pass
