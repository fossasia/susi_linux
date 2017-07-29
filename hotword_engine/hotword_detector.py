"""This module defines an abstract class for Hotword Detection. Any Hotword Detection Engine
implemented in the app must inherit from this class.
HotwordDetector subclasses from threading.Thread since Hotword Detection will run in a separate
thread which will pass callback functions to main in a callback queue which main thread can execute.
"""
import os
from abc import ABC, abstractclassmethod
from threading import Thread
from queue import Queue
from utils.susi_config import config


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

    def __init__(self, callback_queue: Queue, detection_callback) -> None:
        Thread.__init__(self)
        self.callback_queue = callback_queue
        self.detection_callback = detection_callback
        self.is_active = False

    @abstractclassmethod
    def run(self):
        """This method is executed on the start of the thread. You may initialize parameters for Hotword Detection
        here and start the recognition in a busy/wait loop since operation is being run on background thread.
        On detecting a hotword, it should call detected_callback which will check if that recognition should
        be considered or not based whether is_active is set True or False
        """
        pass

    def start_detection(self):
        """Execute this method when recognition needs to start. This method sets `is_active` to True.
        """
        self.is_active = True

    def pause_detection(self):
        """Execute this method when recognition needs to be paused. This method sets `is_active` to False.
        """
        self.is_active = False

    def on_detected(self):
        """This callback is fired when a Hotword Detector detects a hotword. Check whether recognition
        is active or not, if yes then put the detection_callback in the callback_queue. Call threading
        can busy/ wait on the queue to call the callback function passed to it.
        :return: None
        """
        if self.is_active:
            self.pause_detection()
            os.system('play {0} &'.format(config['detection_bell_sound']))
            self.callback_queue.put(self.detection_callback)
