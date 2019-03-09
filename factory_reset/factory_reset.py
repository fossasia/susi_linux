import os
import time
import logging
import subprocess  # nosec #pylint-disable type: ignore

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)
current_folder = os.path.dirname(os.path.abspath(__file__))
factory_reset = '/home/pi/SUSI.AI/susi_linux/factory_reset/factory_reset.sh'

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    i = 1
    while True:
        if GPIO.input(17) == 1:
            time.sleep(0.2)
            pass
        elif GPIO.input(17) == 0 :
            start = time.time()
            while GPIO.input(17) == 0 :
                time.sleep(0.2)
            end = time.time()
            total = end - start
            if total >= 10 :
                print("FACTORY RESET")
                subprocess.Popen(['sudo','bash', factory_reset])
            logger.info(total)
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
