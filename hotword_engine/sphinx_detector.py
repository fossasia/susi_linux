from pocketsphinx import LiveSpeech
from .hotword_detector import HotwordDetector


class PocketSphinxDetector(HotwordDetector):
    def __init__(self, detection_callback) -> None:
        super().__init__(detection_callback)
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
            self.detection_callback()
        else:
            print("Detect kiya tha, but kaam ka nhi h to ignore")
