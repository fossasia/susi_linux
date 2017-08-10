""" Implementation of PocketSphinx Detector with PocketSphinx Speech Recognition Engine.
It works on all the devices.
"""
from pocketsphinx import LiveSpeech

from .hotword_detector import HotwordDetector


class PocketSphinxDetector(HotwordDetector):
    """ This class implements Hotword Detection with the help of LiveSpeech Keyword spotting
    capabilities of PocketSphinx Speech Recognition Engine.
    """
    def __init__(self) -> None:
        super().__init__()
        self.liveSpeech = LiveSpeech(lm=False, keyphrase='susi', kws_threshold=1e-20)

    def run(self):
        """ Implementation of run abstract method in HotwordDetector. This method is called when thread
        is started for the first time. We start the PocketSphinx LiveSpeech Keyword Spotting for
        detecting keyword 'susi'
        """
        for phrase in self.liveSpeech:
            print(phrase)
            if str(phrase) == 'susi':
                self.on_detected()
