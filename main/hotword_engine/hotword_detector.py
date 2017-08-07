"""This module defines an abstract class for Hotword Detection. Any Hotword Detection Engine
implemented in the app must inherit from this class.
HotwordDetector subclasses from threading.Thread since Hotword Detection will run in a separate thread for non-blocking
operation.
"""
from abc import ABC, abstractclassmethod
from threading import Thread

from rx.subjects import Subject


class HotwordDetector(ABC, Thread):
    """ This is an abstract class for a Hotword Detector. Any hotword detector implemented
    in the app must inherit this. It subclasses from threading.Thread allowing Hotword Detection to
    run on a separate thread.
    :attributes
        callback_queue : A queue to send callbacks to main thread.
        detection_callback: A callback function to be called on the calling thread when hotword is detected.
        is_active: A boolean to indicate if hotword detection is currently active. If inactive, the engine ignores
        all the hotword detected in that time.
    """

    def __init__(self) -> None:
        Thread.__init__(self)
        self.subject = Subject()

    @abstractclassmethod
    def run(self):
        """This method is executed on the start of the thread. You may initialize parameters for Hotword Detection
        here and start the recognition in a busy/wait loop since operation is being run on background thread.
        On detecting a hotword, it should call on_detected.
        """
        pass

    def on_detected(self):
        """This callback is fired when a Hotword Detector detects a hotword.
        :return: None
        """
        self.subject.on_next("Hotword")
