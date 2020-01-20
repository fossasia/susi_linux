from abc import ABC, abstractclassmethod
from threading import Thread
from rx.subject import Subject


class WakeButton(ABC, Thread):

    def __init__(self):
        super().__init__()
        self.subject = Subject()

    @abstractclassmethod
    def run(self):
        pass

    def on_detected(self):
        self.subject.on_next("Hotword")
