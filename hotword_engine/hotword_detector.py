from abc import ABC, abstractclassmethod
from threading import Thread


class HotwordDetector(ABC, Thread):
    def __init__(self, detection_callback) -> None:
        Thread.__init__(self)
        self.detection_callback = detection_callback
        self.is_active = False

    @abstractclassmethod
    def run(self):
        pass

    @abstractclassmethod
    def start_detection(self):
        pass

    @abstractclassmethod
    def pause_detection(self):
        pass







