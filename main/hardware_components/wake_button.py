from abc import ABC, abstractclassmethod
from threading import Thread


class WakeButton(ABC, Thread):
    def __init__(self):
        super().__init__()

    @abstractclassmethod
    def run(self):
        pass

    def on_detected(self):
        self.subject.on_next("Hotword")
