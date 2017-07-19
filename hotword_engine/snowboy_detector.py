from .hotword_detector import HotwordDetector
from .snowboy import snowboydecoder
import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "snowboy/resources/susi.pmdl")


class SnowboyDetector(HotwordDetector):
    def __init__(self, detection_callback) -> None:
        super().__init__(detection_callback)
        self.detector = snowboydecoder.HotwordDetector(RESOURCE_FILE, sensitivity=0.5)

    def run(self):
        self.detector.start(detected_callback=self.detected_callback)

    def start_detection(self):
        print("started")
        self.is_active = True
        pass

    def pause_detection(self):
        print("paused")
        self.is_active = False
        pass

    def detected_callback(self):
        if self.is_active:
            self.pause_detection()
            self.detection_callback()
        else:
            print("Detect kiya tha, but kaam ka nhi h to ignore")
