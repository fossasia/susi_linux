from .hotword_detector import HotwordDetector
from .snowboy import snowboydecoder
from queue import Queue
import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "snowboy/resources/susi.pmdl")


class SnowboyDetector(HotwordDetector):
    def __init__(self, callback_queue: Queue, detection_callback) -> None:
        super().__init__(callback_queue, detection_callback)
        self.detector = snowboydecoder.HotwordDetector(RESOURCE_FILE, sensitivity=0.5)

    def run(self):
        self.detector.start(detected_callback=self.detected_callback)

    def start_detection(self):
        self.is_active = True

    def pause_detection(self):
        self.is_active = False

    def detected_callback(self):
        if self.is_active:
            self.pause_detection()
            self.callback_queue.put(self.detection_callback)
