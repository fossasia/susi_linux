"""Implementation of SnowboyDetector using Snowboy Hotword Detection Engine.
It provides excellent recognition of Hotword but all devices are not supported presently.
Use PocketSphinx if you face errors with this Detector.
"""
import os

from .hotword_detector import HotwordDetector
from .snowboy import snowboydecoder

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "snowboy/resources/susi.pmdl")


class SnowboyDetector(HotwordDetector):
    """This implements the Hotword Detector with Snowboy Hotword Detection Engine."""

    def __init__(self) -> None:
        super().__init__()
        self.detector = snowboydecoder.HotwordDetector(RESOURCE_FILE, sensitivity=0.5)

    def run(self):
        """ Implementation of run abstract method in HotwordDetector. This method is called when thread
        is started for the first time. We start the Snowboy detection and declare detected callback as
        detection_callback method declared in parent class.
        """
        self.detector.start(detected_callback=self.on_detected)
