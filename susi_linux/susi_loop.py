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
import json
import speech_recognition
from speech_recognition import Recognizer, Microphone
# from requests.exceptions import ConnectionError

import susi_python as susi
from .hardware_components.lights import lights
from .internet_test import internet_on
from .action_scheduler import ActionScheduler
from .player import player
from susi_config import SusiConfig
from .speech import TTS

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("This device doesn't have GPIO port")
    GPIO = None

class SusiLoop():
    """The main SUSI loop dealing with hotword detection, voice recognition,
    server communication, action processing, etc"""

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
        recognizer.energy_threshold = 2000
        self.recognizer = recognizer
        self.susi = susi
        self.renderer = renderer
        self.server_url = "https://127.0.0.1:4000"
        self.action_schduler = ActionScheduler()
        self.action_schduler.start()
        self.event_queue = queue.Queue()
        self.idle = True
        self.supported_languages = None

        try:
            res = requests.get('http://ip-api.com/json').json()
            self.susi.update_location(
                longitude=res['lon'], latitude=res['lat'],
                country_name=res['country'], country_code=res['countryCode'])

        except ConnectionError as e:
            logger.error(e)

        self.susi_config = SusiConfig()
        self.lang = self.susi_config.get('language')
        self.path_base = self.susi_config.get('path.base')
        self.sound_detection = os.path.abspath(
                                   os.path.join(self.path_base,
                                                self.susi_config.get('path.sound.detection')))
        self.sound_problem = os.path.abspath(
                                   os.path.join(self.path_base,
                                                self.susi_config.get('path.sound.problem')))
        self.sound_error_recognition = os.path.abspath(
                                   os.path.join(self.path_base,
                                                self.susi_config.get('path.sound.error.recognition')))
        self.sound_error_timeout = os.path.abspath(
                                   os.path.join(self.path_base,
                                                self.susi_config.get('path.sound.error.timeout')))

        if self.susi_config.get('susi.mode') == 'authenticated':
            try:
                susi.sign_in(email=self.susi_config.get('susi.user'),
                             password=self.susi_config.get('susi.pass'))
            except Exception as e:
                logger.error('Some error occurred in login. Check you login details with susi-config.\n%s', e)

        if self.susi_config.get('hotword.engine') == 'Snowboy':
            from .hotword_engine.snowboy_detector import SnowboyDetector
            hotword_model = "susi.pmdl"
            if self.susi_config.get('hotword.model'):
                logger.debug("Using configured hotword model: " + self.susi_config.get('hotword.model'))
                hotword_model = self.susi_config.get('hotword_model')
            self.hotword_detector = SnowboyDetector(model=hotword_model)
        elif self.susi_config.get('hotword.engine') == 'PocketSphinx':
            from .hotword_engine.sphinx_detector import PocketSphinxDetector
            self.hotword_detector = PocketSphinxDetector()
        elif self.susi_config.get('hotword.engine') == 'None':
            self.hotword_detector = None
        else:
            raise ValueError(f"Unrecognized value for hotword.engine: {self.susi_config.get('hotword.engine')}")

        if self.susi_config.get('wakebutton') == 'enabled':
            logger.info("Susi has the wake button enabled")
            if self.susi_config.get('device') == 'RaspberryPi':
                logger.info("Susi runs on a RaspberryPi")
                from .hardware_components.rpi_wake_button import RaspberryPiWakeButton
                self.wake_button = RaspberryPiWakeButton()
            else:
                logger.warning("Susi is not running on a RaspberryPi")
                self.wake_button = None
        else:
            logger.warning("Susi has the wake button disabled")
            self.wake_button = None


        stt = self.susi_config.get('stt')
        if stt == 'google' or stt == 'watson' or stt == 'bing':
            # for internet based services we assume any language supported
            self.supported_languages = None
        elif stt == 'pocketsphinx':
            ps_data_dir = os.path.join(os.path.dirname(os.path.realpath(speech_recognition.__file__)), "pocketsphinx-data")
            self.supported_languages = [ f.name for f in os.scandir(ps_data_dir) if f.is_dir() ]
            logger.debug(f"Found supported languages for PocketSphinx: {self.supported_languages}")
        elif stt == 'deepspeech-local':
            ds_data_dir = os.path.join(os.path.dirname(os.path.realpath(speech_recognition.__file__)), "deepspeech-data")
            self.supported_languages = [ f.name for f in os.scandir(ds_data_dir) if f.is_dir() ]
            logger.debug(f"Found supported languages for DeepSpeech: {self.supported_languages}")
        elif stt == 'vosk':
            vosk_data_dir = os.path.join(os.path.dirname(os.path.realpath(speech_recognition.__file__)), "vosk-data")
            self.vosk_base_model_dir = vosk_data_dir
            self.supported_languages = [ f.name for f in os.scandir(vosk_data_dir) if f.is_dir() ]
            logger.debug(f"Found supported languages for Vosk: {self.supported_languages}")
            if (not self.lang in self.supported_languages):
                self.lang = "en"
            from vosk import Model
            self.vosk_model = Model(f"{vosk_data_dir}/{self.lang}")
        else:
            self.supported_languages = None
            logger.warn(f"Unknown stt setting: {stt}")

        if self.susi_config.get('stt') == 'deepspeech-local':
            self.microphone = Microphone(sample_rate=16000)
        else:
            self.microphone = Microphone()

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


    def start(self, background = False):
        """ start processing of audio events """
        if self.hotword_detector is not None:
            hotword_thread = Thread(target=self.hotword_listener, name="HotwordDetectorThread")
            hotword_thread.daemon = True
            hotword_thread.start()

        if background:
            queue_loop_thread = Thread(target=self.queue_loop, name="QueueLoopThread")
            queue_loop_thread.daemon = True
            queue_loop_thread.start()
        else:
            self.queue_loop()

    
    def queue_loop(self):
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
        player.beep(self.sound_detection)

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
                logger.debug("delaying idle setting for 0.05s")
                Timer(interval=0.05, function=self.set_idle).start()
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
        self.notify_renderer('idle')
        self.idle = True

    def __speak(self, text):
        """Method to set the default TTS for the Speaker"""
        tts = self.susi_config.get('tts')
        if tts == 'google':
            TTS.speak_google_tts(text)
        elif tts == 'flite':
            logger.info("Using flite for TTS")  # indication for using an offline music player
            TTS.speak_flite_tts(text)
        elif tts == 'watson':
            TTS.speak_watson_tts(text)
        else:
            raise ValueError("unknown key for tts", tts)

    def recognize_audio(self, recognizer, audio):
        """Use the configured STT method to convert spoken audio to text"""
        stt = self.susi_config.get('stt')
        lang = self.susi_config.get('language')
        # Try to adjust language to what is available
        # None indicates any language supported, so use it as is
        if self.supported_languages is not None:
            if len(self.supported_languages) == 0:
                raise ValueError(f"No supported language for the current STT {stt}")
            if "en-US" in self.supported_languages:
                default = "en-US"
            else:
                default = self.supported_languages[0]
            if lang not in self.supported_languages:
                if len(lang) < 2:
                    logger.warn(f"Unsupported language code {lang}, using {default}")
                    lang = default
                else:
                    langshort = lang[0:2].lower()
                    for l in self.supported_languages:
                        if langshort == l[0:2].lower():
                            logger.debug(f"Using language code {l} instead of {lang}")
                            lang = l
                            break
            # We should now have a proper language code in lang, if not, warn and reset
            if lang not in self.supported_languages:
                logger.warn(f"Unsupported langauge code {lang}, using {default}")
                lang = default

        logger.info("Trying to recognize audio with %s in language: %s", stt, lang)
        if stt == 'google':
            return recognizer.recognize_google(audio, language=lang)

        elif stt == 'watson':
            username = self.susi_config.get('watson.stt.user')
            password = self.susi_config.get('watson.stt.pass')
            return recognizer.recognize_ibm(
                username=username, password=password, language=lang, audio_data=audio)

        elif stt == 'pocket_sphinx':
            return recognizer.recognize_sphinx(audio, language=lang)

        elif stt == 'bing':
            api_key = self.susi_config.get('bing.api')
            return recognizer.recognize_bing(audio_data=audio, key=api_key, language=lang)

        elif stt == 'deepspeech-local':
            return recognizer.recognize_deepspeech(audio, language=lang)

        elif stt == 'vosk':
            # TODO language support not implemented, we always use
            # the first language
            recognizer.vosk_model = self.vosk_model
            ret = json.loads(recognizer.recognize_vosk(audio, language=lang))
            if ("text" in ret):
                return ret["text"]
            else:
                logger.error("Cannot detect text")
                return ""

        else:
            logger.error(f"Unknown STT setting: {stt}")
            logger.error("Using DeepSpeech!")
            return recognizer.recognize_deepspeech(audio, language=lang)



    def deal_with_error(self, payload=None):
        """deal with errors happening during processing of audio events"""
        if payload == 'RecognitionError':
            logger.debug("ErrorState Recognition Error")
            self.notify_renderer('error', 'recognition')
            lights.speak()
            player.say(self.sound_error_recognition)
            lights.off()
        elif payload == 'ConnectionError':
            self.notify_renderer('error', 'connection')
            self.susi_config.set('tts', 'flite')
            self.susi_config.set('stt', 'pocketsphinx')
            print("Internet Connection not available")
            lights.speak()
            lights.off()
            logger.info("Changed to offline providers")

        elif payload == 'ListenTimeout':
            self.notify_renderer('error', 'timeout')
            lights.speak()
            player.say(self.sound_error_timeout)
            lights.off()

        else:
            print("Error: {} \n".format(payload))
            self.notify_renderer('error')
            lights.speak()
            player.say(self.sound_problem)
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

            self.notify_renderer('speaking', payload={'susi_reply': reply})

            if 'planned_actions' in reply.keys():
                logger.debug("planning action: ")
                for plan in reply['planned_actions']:
                    logger.debug("plan = " + str(plan))
                    # plan answers look like this:
                    # plan = {'planned_actions': [{'language': 'en', 'answer': 'ALARM', 'plan_delay': 300001,
                    #   'plan_date': '2020-01-09T02:05:10.377Z'}], 'language': 'en', 'answer': 'alarm set for in 5 minutes'}
                    # we use time.time as timefunc for scheduler, so we need to convert the
                    # delay and absolute time to the same format, that is float of sec since epoch
                    # Unfortunately, Python is tooooooo stupid to provide ISO standard confirm standard
                    # library. datetime.fromisoformat sounds like perfectly made, only that it doesn't
                    # parse the Z postfix, congratulations.
                    # https://discuss.python.org/t/parse-z-timezone-suffix-in-datetime/2220
                    # Replace it manually with +00:00
                    # We send both the delay and absolute time in case one of the two is missing
                    # the scheduler prefers the delay value
                    plan_date_sec = datetime.fromisoformat(re.sub('Z$', '+00:00', plan['plan_date'])).timestamp()
                    self.action_schduler.add_event(int(plan['plan_delay']) / 1000, plan_date_sec, plan)

            # first responses WITHOUT answer key!

            # {'answer': 'Audio volume is now 10 percent.', 'volume': '10'}
            if 'volume' in reply.keys():
                no_answer_needed = True
                player.volume(reply['volume'])
                player.say(self.sound_detection)

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
                if answer_lang != self.susi_config.get("language"):
                    logger.info("Switching language to: %s", answer_lang)
                    # switch language
                    self.susi_config.set('language', answer_lang)

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

