"""This module declares the SUSI State Machine Class and Component Class.
The SUSI State Machine works on the concept of Finite State Machine.
"""
import time
import logging
from threading import Thread
from urllib.parse import urljoin

import requests
import json_config
import os
import speech_recognition
from speech_recognition import Recognizer, Microphone
from requests.exceptions import ConnectionError

import susi_python as susi
from .busy_state import BusyState
from .error_state import ErrorState
from .idle_state import IdleState
from .recognizing_state import RecognizingState
from ..scheduler import ActionScheduler


logger = logging.getLogger(__name__)


class Components:
    """Common components accessible by each state of the the  SUSI state Machine.
    """

    def __init__(self, renderer=None):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(27, GPIO.OUT)
            GPIO.setup(22, GPIO.OUT)
        except ImportError:
            logger.warning("This device doesn't have GPIO port")
        except RuntimeError as e:
            logger.error(e)
            pass
        thread1 = Thread(target=self.server_checker, name="Thread1")
        thread1.daemon = True
        thread1.start()

        recognizer = Recognizer()
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 1000
        self.recognizer = recognizer
        self.microphone = Microphone()
        self.susi = susi
        self.renderer = renderer
        self.server_url = "https://127.0.0.1:4000"
        self.action_schduler = ActionScheduler()
        self.action_schduler.start()

        try:
            res = requests.get('http://ip-api.com/json').json()
            self.susi.update_location(
                longitude=res['lon'], latitude=res['lat'],
                country_name=res['country'], country_code=res['countryCode'])

        except ConnectionError as e:
            logger.error(e)

        self.config = json_config.connect('config.json')

        if self.config['usage_mode'] == 'authenticated':
            try:
                susi.sign_in(email=self.config['login_credentials']['email'],
                             password=self.config['login_credentials']['password'])
            except Exception as e:
                logger.error('Some error occurred in login. Check you login details in config.json.\n%s', e)

        if self.config['hotword_engine'] == 'Snowboy':
            from ..hotword_engine.snowboy_detector import SnowboyDetector
            self.hotword_detector = SnowboyDetector()
        else:
            from ..hotword_engine.sphinx_detector import PocketSphinxDetector
            self.hotword_detector = PocketSphinxDetector()

        if self.config['WakeButton'] == 'enabled':
            logger.info("Susi has the wake button enabled")
            if self.config['Device'] == 'RaspberryPi':
                logger.info("Susi runs on a RaspberryPi")
                from ..hardware_components import RaspberryPiWakeButton
                self.wake_button = RaspberryPiWakeButton()
            else:
                logger.warning("Susi is not running on a RaspberryPi")
                self.wake_button = None
        else:
            logger.warning("Susi has the wake button disabled")
            self.wake_button = None

        # determine PocketSphinx supported languages
        self.pocketsphinx_supported_langs = os.listdir(os.path.dirname(speech_recognition.__file__) + '/pocketsphinx-data')

    def server_checker(self):
        response_one = None
        test_params = {
            'q': 'Hello',
            'timezoneOffset': int(time.timezone / 60)
        }
        while response_one is None:
            try:
                url = urljoin(self.server_url, '/susi/chat.json')
                response_one = requests.get(url, test_params).result()
                api_endpoint = self.server_url
                susi.use_api_endpoint(api_endpoint)
            except AttributeError:
                time.sleep(10)
                continue
            except ConnectionError:
                time.sleep(10)
                continue


class SusiStateMachine(Thread):
    """SUSI State Machine works on the concept of Finite State Machine. Each step of working of this app is divided into
    a state of the State Machine. Each state can transition into one of the allowed states and pass some information
    to other states as PAYLOAD. Upon Error, transition should happen to Error State and after speaking the correct error
    message, the machine transitions to the Idle State.
    """

    def __init__(self, renderer=None):
        super().__init__()
        components = Components(renderer)
        self.__idle_state = IdleState(components)
        self.__recognizing_state = RecognizingState(components)
        self.__busy_state = BusyState(components)
        self.__error_state = ErrorState(components)
        self.current_state = self.__idle_state

        self.__idle_state.allowedStateTransitions = \
            {'recognizing': self.__recognizing_state, 'error': self.__error_state, 'busy': self.__busy_state}
        self.__recognizing_state.allowedStateTransitions = \
            {'busy': self.__busy_state, 'error': self.__error_state}
        self.__busy_state.allowedStateTransitions = \
            {'idle': self.__idle_state, 'error': self.__error_state, 'recognizing': self.__recognizing_state}
        self.__error_state.allowedStateTransitions = \
            {'idle': self.__idle_state}

    def run(self):
        self.current_state.on_enter(payload=None)
