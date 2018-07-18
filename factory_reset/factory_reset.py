import time
import RPi.GPIO as GPIO
import os
import subprocess  # nosec #pylint-disable type: ignore
import alsaaudio


current_folder = os.path.dirname(os.path.abspath(__file__))
factory_reset = os.path.join(current_folder,'factory_reset.sh')
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN)
    i = 1
    while True:
        if GPIO.input(17) == 1:
            pass
        elif GPIO.input(17) == 0 :
            start = time.time()
            while GPIO.input(17) == 0 :
                time.sleep(0.1)
            end = time.time()
            total = end - start
            if total >= 7 :
                subprocess.call(['bash','factory_reset.sh'])  # nosec #pylint-disable type: ignore
            else :
                mixer = alsaaudio.Mixer()
                value = mixer.getvolume()[0]
                if value != 0:
                    mixer.setvolume(0)
                else:
                    mixer.setvolume(50)
            print(total)
            time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
