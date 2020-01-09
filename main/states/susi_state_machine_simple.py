"""
Processing logic of susi_linux
"""
import time
import os
import re
import logging
import queue
from threading import Thread, Timer, current_thread
from datetime import datetime
from urllib.parse import urljoin
import speech_recognition as sr
import requests
import json_config
from speech_recognition import Recognizer, Microphone
# from requests.exceptions import ConnectionError

import susi_python as susi
from .lights import lights
from .internet_test import internet_on
from ..scheduler import ActionScheduler
from ..player import player
from ..config import susi_config
from ..speech import TTS

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("This device doesn't have GPIO port")
    GPIO = None

# needed for backward compatibility with import statements
class Components():
    """Dummy class necessary for backward compatibility with old code"""
    pass

class SusiStateMachine():
    """Actually not a state machine, but we keep the name for now"""

    def __init__(self, renderer=None):
        if GPIO:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(27, GPIO.OUT)
                GPIO.setup(22, GPIO.OUT)
            except RuntimeError as e:
                logger.error(e)

        thread1 = Thread(target=self.server_checker, name="ServerCheckerThread")
        thread1.daemon = True
        thread1.start()

        recognizer = Recognizer()
        # this was False in the old state machine, but reading the API docs
        # https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst
        # it seems that True is actually better!
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 1000
        self.recognizer = recognizer
        self.microphone = Microphone()
        self.susi = susi
        self.renderer = renderer
        self.server_url = "https://127.0.0.1:4000"
        self.action_schduler = ActionScheduler()
        self.action_schduler.start()
        self.event_queue = queue.Queue()
        self.idle = True

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
            hotword_model = "susi.pmdl"
            if self.config['hotword_model']:
                logger.debug("Using configured hotword model: " + self.config['hotword_model'])
                hotword_model = self.config['hotword_model']
            self.hotword_detector = SnowboyDetector(model=hotword_model)
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

        if self.hotword_detector is not None:
            self.hotword_detector.subject.subscribe(
                on_next=lambda x: self.hotword_detected_callback())
        if self.wake_button is not None:
            self.wake_button.subject.subscribe(
                on_next=lambda x: self.hotword_detected_callback())
        if self.renderer is not None:
            self.renderer.subject.subscribe(
                on_next=lambda x: self.hotword_detected_callback())
        if self.action_schduler is not None:
            self.action_schduler.subject.subscribe(
                on_next=lambda x: self.queue_event(x))

    def queue_event(self, event):
        """ queue a delayed event"""
        self.event_queue.put(event)

    def hotword_listener(self):
        """ thread function for listening to the hotword"""
        # this function never returns ...
        self.hotword_detector.start()

    def server_checker(self):
        """ thread function for checking the used server being alive"""
        response_one = None
        test_params = {
            'q': 'Hello',
            'timezoneOffset': int(time.timezone / 60)
        }
        while response_one is None:
            try:
                logger.debug("checking for local server")
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


    def start(self):
        """ start processing of audio events """
        hotword_thread = Thread(target=self.hotword_listener, name="HotwordDetectorThread")
        hotword_thread.daemon = True
        hotword_thread.start()

        while True:
            # block until events are available
            ev = self.event_queue.get(block = True)
            logger.debug("Got event from event queue, trying to deal with it")
            # wait until idle
            while True:
                logger.debug("Waiting to become idle for planned action")
                if not self.idle:
                    time.sleep(1)
                    continue
                logger.debug("We are idle now ...")
                self.idle = False
                self.deal_with_answer(ev)
                # back from processing
                player.restore_softvolume()
                if GPIO:
                    try:
                        GPIO.output(27, False)
                        GPIO.output(22, False)
                    except RuntimeError:
                        pass
                self.idle = True
                break


    def notify_renderer(self, message, payload=None):
        """ notify program renderer """
        if self.renderer is not None:
            self.renderer.receive_message(message, payload)

    def hotword_detected_callback(self):
        """
        Callback when the hotword is detected. Does the full processing
        logic formerly contained in different states
        """
        logger.debug("Entering hotword callback")
        # don't do anything if we are already busy
        if not self.idle:
            logger.debug("Callback called while already busy, returning immediately from callback")
            return

        logger.debug("We are idle, so work on it!")
        self.idle = False

        # beep
        player.beep(os.path.abspath(os.path.join(self.config['data_base_dir'],
                                                 self.config['detection_bell_sound'])))
        if GPIO:
            GPIO.output(22, True)
        audio = None
        logger.debug("notify renderer for listening")
        self.notify_renderer('listening')
        with self.microphone as source:
            try:
                logger.debug("listening to voice command")
                audio = self.recognizer.listen(source, timeout=10.0, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                logger.debug("timeout reached waiting for voice command")
                self.deal_with_error('ListenTimeout')
                return
        if GPIO:
            GPIO.output(22, False)

        lights.off()
        lights.think()
        try:
            logger.debug("Converting audio to text")
            value = self.recognize_audio(audio=audio, recognizer=self.recognizer)
            logger.debug("recognize_audio => %s", value)
            self.notify_renderer('recognized', value)
            if self.deal_with_answer(value):
                pass
            else:
                logger.error("Error dealing with answer")

        except sr.UnknownValueError as e:
            logger.error("UnknownValueError from SpeechRecognition: %s", e)
            self.deal_with_error('RecognitionError')

        logger.debug("delaying idle setting for 0.05s")
        Timer(interval=0.05, function=self.set_idle).start()
        return

    def set_idle(self):
        logger.debug("Switching to idle mode")
        self.idle = True

    def __speak(self, text):
        """Method to set the default TTS for the Speaker"""
        if self.config['default_tts'] == 'google':
            TTS.speak_google_tts(text)
        if self.config['default_tts'] == 'flite':
            logger.info("Using flite for TTS")  # indication for using an offline music player
            TTS.speak_flite_tts(text)
        elif self.config['default_tts'] == 'watson':
            TTS.speak_watson_tts(text)

    def recognize_audio(self, recognizer, audio):
        """Use the configured STT method to convert spoken audio to text"""
        logger.info("Trying to recognize audio with %s in language: %s",
                    self.config['default_stt'], susi_config["language"])
        if self.config['default_stt'] == 'google':
            return recognizer.recognize_google(audio, language=susi_config["language"])

        elif self.config['default_stt'] == 'watson':
            username = self.config['watson_stt_config']['username']
            password = self.config['watson_stt_config']['password']
            return recognizer.recognize_ibm(
                username=username,
                password=password,
                language=susi_config["language"],
                audio_data=audio)

        elif self.config['default_stt'] == 'pocket_sphinx':
            lang = susi_config["language"].replace("_", "-")
            if internet_on():
                self.config['default_stt'] = 'google'
                return recognizer.recognize_google(audio, language=lang)
            else:
                return recognizer.recognize_sphinx(audio, language=lang)

        elif self.config['default_stt'] == 'bing':
            api_key = self.config['bing_speech_api_key']
            return recognizer.recognize_bing(audio_data=audio, key=api_key,
                                             language=susi_config["language"])

        elif self.config['default_stt'] == 'deepspeech-local':
            lang = susi_config["language"].replace("_", "-")
            return recognizer.recognize_deepspeech(audio, language=lang)

        else:
            logger.error("Unknown STT setting: " + self.config['default_stt'])
            logger.error("Using Google!")
            return recognizer.recognize_google(audio, language=susi_config["language"])



    def deal_with_error(self, payload=None):
        """deal with errors happening during processing of audio events"""
        if payload == 'RecognitionError':
            logger.debug("ErrorState Recognition Error")
            self.notify_renderer('error', 'recognition')
            lights.speak()
            player.say(os.path.abspath(os.path.join(self.config['data_base_dir'],
                                                    self.config['recognition_error_sound'])))
            lights.off()
        elif payload == 'ConnectionError':
            self.notify_renderer('error', 'connection')
            susi_config['default_tts'] = 'flite'
            susi_config['default_stt'] = 'pocket_sphinx'
            print("Internet Connection not available")
            lights.speak()
            lights.off()
            logger.info("Changed to offline providers")

        elif payload == 'ListenTimeout':
            self.notify_renderer('error', 'timeout')
            lights.speak()
            player.say(os.path.abspath(os.path.join(self.config['data_base_dir'],
                                                    self.config['timeout_error_sound'])))
            lights.off()

        else:
            print("Error: {} \n".format(payload))
            self.notify_renderer('error')
            lights.speak()
            player.say(os.path.abspath(os.path.join(self.config['data_base_dir'],
                                                    self.config['problem_sound'])))
            lights.off()


    def deal_with_answer(self, payload=None):
        """processing logic - how to deal with answers from the server"""
        try:
            no_answer_needed = False

            if isinstance(payload, str):
                logger.debug("Sending payload to susi server: %s", payload)
                reply = self.susi.ask(payload)
            else:
                logger.debug("Executing planned action response: %s", payload)
                reply = payload

            if GPIO:
                GPIO.output(27, True)
            if self.renderer is not None:
                self.notify_renderer('speaking', payload={'susi_reply': reply})

            if 'planned_actions' in reply.keys():
                logger.debug("planning action: ")
                for plan in reply['planned_actions']:
                    logger.debug("plan = " + str(plan))
                    # plan answers look like this:
                    # plan = {'language': 'en', 'answer': 'ALARM', 'plan_delay': 0,
                    #         'plan_date': '2019-12-30T13:36:05.458Z'}
                    # we use time.time as timefunc for scheduler, so we need to convert the
                    # delay and absolute time to the same format, that is float of sec since epoch
                    # Unfortunately, Python is tooooooo stupid to provide ISO standard confirm standard
                    # library. datetime.fromisoformat sounds like perfectly made, only that it doesn't
                    # parse the Z postfix, congratulations.
                    # https://discuss.python.org/t/parse-z-timezone-suffix-in-datetime/2220
                    # Replace it manually with +00:00
                    plan_date_sec = datetime.fromisoformat(re.sub('Z$', '+00:00', plan['plan_date'])).timestamp()
                    self.action_schduler.add_event(int(plan['plan_delay']) / 1000, plan_date_sec, plan)

            # first responses WITHOUT answer key!

            # {'answer': 'Audio volume is now 10 percent.', 'volume': '10'}
            if 'volume' in reply.keys():
                no_answer_needed = True
                player.volume(reply['volume'])
                player.say(os.path.abspath(os.path.join(self.config['data_base_dir'],
                                                        self.config['detection_bell_sound'])))

            if 'media_action' in reply.keys():
                action = reply['media_action']
                if action == 'pause':
                    no_answer_needed = True
                    player.pause()
                    lights.off()
                    lights.wakeup()
                elif action == 'resume':
                    no_answer_needed = True
                    player.resume()
                elif action == 'restart':
                    no_answer_needed = True
                    player.restart()
                elif action == 'next':
                    no_answer_needed = True
                    player.next()
                elif action == 'previous':
                    no_answer_needed = True
                    player.previous()
                elif action == 'shuffle':
                    no_answer_needed = True
                    player.shuffle()
                else:
                    logger.error('Unknown media action: %s', action)

            # {'stop': <susi_python.models.StopAction object at 0x7f4641598d30>}
            if 'stop' in reply.keys():
                no_answer_needed = True
                player.stop()

            if 'answer' in reply.keys():
                logger.info('Susi: %s', reply['answer'])
                lights.off()
                lights.speak()
                self.__speak(reply['answer'])
                lights.off()
            else:
                if not no_answer_needed and 'identifier' not in reply.keys():
                    lights.off()
                    lights.speak()
                    self.__speak("I don't have an answer to this")
                    lights.off()

            if 'language' in reply.keys():
                answer_lang = reply['language']
                if answer_lang != susi_config["language"]:
                    logger.info("Switching language to: %s", answer_lang)
                    # switch language
                    susi_config["language"] = answer_lang

            # answer to "play ..."
            # {'identifier': 'ytd-04854XqcfCY', 'answer': 'Playing Queen -  We Are The Champions (Official Video)'}
            if 'identifier' in reply.keys():
                url = reply['identifier']
                logger.debug("Playing " + url)
                if url[:3] == 'ytd':
                    player.playytb(url[4:])
                else:
                    player.play(url)

            if 'table' in reply.keys():
                table = reply['table']
                for h in table.head:
                    print('%s\t' % h, end='')
                    self.__speak(h)
                print()
                for datum in table.data[0:4]:
                    for value in datum:
                        print('%s\t' % value, end='')
                        self.__speak(value)
                    print()

            if 'rss' in reply.keys():
                rss = reply['rss']
                entities = rss['entities']
                count = rss['count']
                for entity in entities[0:count]:
                    logger.debug(entity.title)
                    self.__speak(entity.title)

        except ConnectionError:
            self.deal_with_error('ConnectionError')
            return False
        except Exception as e:
            logger.error('Unknown error: %s', e)
            return False

        return True

