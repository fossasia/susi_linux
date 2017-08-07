import os
from abc import ABC, abstractclassmethod
from queue import Queue
from threading import Thread

from utils.susi_config import config


class WakeButton(ABC, Thread):
    def __init__(self, detection_callback, callback_queue: Queue):
        super().__init__()
        self.detection_callback = detection_callback
        self.callback_queue = callback_queue
        self.is_active = False

    @abstractclassmethod
    def run(self):
        pass

    def on_detected(self):
        if self.is_active:
            self.callback_queue.put(self.detection_callback)
            os.system('play {0} &'.format(config['detection_bell_sound']))
            self.is_active = False
