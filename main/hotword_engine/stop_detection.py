"""Implementation of SnowboyDetector using Snowboy Hotword Detection Engine.
This method is to support Second query processing using snowboy
"""

from snowboy import snowboydecoder
import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "susi.pmdl")


class StopDetector():
    """This implements the Stop Detection with Snowboy Hotword Detection Engine."""

    def __init__(self, detection) -> None:
        super().__init__()
        self.detector = snowboydecoder.HotwordDetector(
            RESOURCE_FILE, sensitivity=0.6)
        self.detection = detection

    def run(self):
        """ Implementation of run abstract method in HotwordDetector. This method is called when thread
        is started for the first time. We start the Snowboy detection and declare detected callback as
        detection_callback method declared in parent class.
        """
        self.detector.start(detected_callback=self.detection)
