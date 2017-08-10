"""This module declares the SUSI State Machine Class and Component Class.
The SUSI State Machine works on the concept of Finite State Machine.
"""
import json_config
from speech_recognition import Recognizer, Microphone

import susi_python as susi
from .busy_state import BusyState
from .error_state import ErrorState
from .recognizing_state import RecognizingState
from .idle_state import IdleState


class Components:
    """Common components accessible by each state of the the  SUSI state Machine.
    """

    def __init__(self):
        recognizer = Recognizer()
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 1000
        self.recognizer = recognizer
        self.microphone = Microphone()
        self.susi = susi
        self.config = json_config.connect('config.json')

        if self.config['hotword_engine'] == 'Snowboy':
            from main.hotword_engine import SnowboyDetector
            self.hotword_detector = SnowboyDetector()
        else:
            from main.hotword_engine import PocketSphinxDetector
            self.hotword_detector = PocketSphinxDetector()

        if self.config['wake_button'] == 'enabled':
            if self.config['device'] == 'RaspberryPi':
                from ..hardware_components import RaspberryPiWakeButton
                self.wake_button = RaspberryPiWakeButton()
            else:
                self.wake_button = None
        else:
            self.wake_button = None


class SusiStateMachine:
    """SUSI State Machine works on the concept of Finite State Machine. Each step of working of this app is divided into
    a state of the State Machine. Each state can transition into one of the allowed states and pass some information
    to other states as PAYLOAD. Upon Error, transition should happen to Error State and after speaking the correct error
    message, the machine transitions to the Idle State.
    """

    def __init__(self):
        super().__init__()
        components = Components()
        self.__idle_state = IdleState(components)
        self.__recognizing_state = RecognizingState(components)
        self.__busy_state = BusyState(components)
        self.__error_state = ErrorState(components)
        self.current_state = self.__idle_state

        self.__idle_state.allowedStateTransitions = \
            {'recognizing': self.__recognizing_state, 'error': self.__error_state}
        self.__recognizing_state.allowedStateTransitions = \
            {'busy': self.__busy_state, 'error': self.__error_state}
        self.__busy_state.allowedStateTransitions = \
            {'idle': self.__idle_state, 'error': self.__error_state}
        self.__error_state.allowedStateTransitions = \
            {'idle': self.__idle_state}

        self.current_state.on_enter(payload=None)
