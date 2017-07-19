from pocketsphinx import LiveSpeech
from .hotword_detector import HotwordDetector
from queue import Queue


class PocketSphinxDetector(HotwordDetector):
    def __init__(self, callback_queue: Queue, detection_callback) -> None:
        super().__init__(callback_queue, detection_callback)
        self.liveSpeech = LiveSpeech(lm=False, keyphrase='susi', kws_threshold=1e-20)

    def run(self):
        for phrase in self.liveSpeech:
            print(phrase)
            if str(phrase) == 'susi':
                self.on_detected()

    def start_detection(self):
        self.is_active = True

    def pause_detection(self):
        self.is_active = False

    def on_detected(self):
        print("detected")
        if self.is_active:
            self.pause_detection()
            self.callback_queue.put(self.detection_callback)
