"""Class to represent the Busy State
"""
import os
import signal
import logging
import subprocess   # nosec #pylint-disable type: ignore

import alsaaudio
import requests

from ..hotword_engine.stop_detection import StopDetector
from ..speech import TTS
from .base_state import State
from .lights import lights

try:
    import RPi.GPIO as GPIO
except:
    pass

logger = logging.getLogger(__name__)


class BusyState(State):
    """Busy state inherits from base class State. In this state, SUSI API is called to perform query and the response
    is then spoken with the selected Text to Speech Service.
    """
    def detection(self):
        """This callback is fired when a Hotword Detector detects a hotword.
        All the songs/videos are paused for a brief moment and then played again.
        :return: None
        """
        # subprocess.call(['killall', 'play'])
        # subprocess.call(['killall', 'mpv']
        if hasattr(self, 'video_process'):
            self.video_process.send_signal(signal.SIGSTOP)  # nosec #pylint-disable type: ignore
            lights.off()
            lights.wakeup()
            subprocess.Popen(['play', str(self.components.config['detection_bell_sound'])])  # nosec #pylint-disable type: ignore
            lights.wakeup()
            self.transition(self.allowedStateTransitions.get('recognizing'))
            self.video_process.send_signal(signal.SIGCONT)  # nosec #pylint-disable type: ignore

        if hasattr(self, 'audio_process'):
            self.audio_process.send_signal(signal.SIGSTOP)  # nosec #pylint-disable type: ignore
            lights.off()
            lights.wakeup()
            subprocess.Popen(['play', str(self.components.config['detection_bell_sound'])])  # nosec #pylint-disable type: ignore
            lights.wakeup()
            self.transition(self.allowedStateTransitions.get('recognizing'))
            self.audio_process.send_signal(signal.SIGCONT)  # nosec #pylint-disable type: ignore

    def song_modulation(self, process, action):
        """ A method to modulate(pause/play/restart) the songs and videos being played through the Speaker.
        """
        actions = { "pause": signal.SIGSTOP, "play": signal.SIGCONT, "stop": signal.SIGKILL }

        if (process == 'video_process'):
            self.video_process.send_signal(actions[action])
            lights.off()
            lights.wakeup()

        elif (process == 'audio_process'):
            self.video_process.send_signal(actions[action])
            lights.off()
            lights.wakeup()

        else:
            logger.debug("No ongoing media process")

    def on_enter(self, payload=None):
        """This method is executed on entry to Busy State. SUSI API is called via SUSI Python library to fetch the
        result. We then call TTS to speak the reply. If successful, we transition to Idle State else to the Error State.
        :param payload: query to be asked to SUSI
        :return: None
        """
        logger.debug('Busy state')
        try:
            reply = self.components.susi.ask(payload)
            if self.useGPIO:
                GPIO.output(27, True)
            if self.components.renderer is not None:
                self.notify_renderer('speaking', payload={'susi_reply': reply})

            if 'answer' in reply.keys():
                logger.info('Susi: %s', reply['answer'])
                lights.off()
                lights.speak()
                self.__speak(reply['answer'])
                lights.off()
            else:
                lights.off()
                lights.speak()
                self.__speak("I don't have an answer to this")
                lights.off()

            if 'identifier' in reply.keys():
                classifier = reply['identifier']
                stopAction = StopDetector(self.detection)
                if classifier[:3] == 'ytd':
                    video_url = reply['identifier']
                    try:
                        x = requests.get('http://localhost:7070/song?vid=' + video_url[4:])
                        data = x.json()
                        url = data['url']
                        video_process = subprocess.Popen(['cvlc', 'https' + url[5:], '--no-video'])
                        self.video_process = video_process
                    except Exception as e:
                        logger.error(e);
                    stopAction.run()
                    stopAction.detector.terminate()

                else:
                    audio_url = reply['identifier']
                    audio_process = subprocess.Popen(['play', audio_url[6:], '--no-show-progress'])  # nosec #pylint-disable type: ignore
                    self.audio_process = audio_process
                    stopAction.run()
                    stopAction.detector.terminate()

            if 'volume' in reply.keys():
                subprocess.call(['amixer', '-c', '1', 'sset', "'Headphone'", ',', '0', str(reply['volume'])])
                subprocess.call(['amixer', '-c', '1', 'sset', "'Speaker'", ',', '0', str(reply['volume'])])
                subprocess.call(['play', str(self.components.config['detection_bell_sound'])])  # nosec #pylint-disable type: ignore

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

            if 'pause' in reply.keys():
                if hasattr(self, 'video_process'):
                    self.song_modulation('video_process', 'pause')
                elif hasattr(self, 'audio_process'):
                    self.song_modulation('audio_process', 'pause')

            if 'resume' in reply.keys():
                if hasattr(self, 'video_process'):
                    self.song_modulation('video_process', 'play')
                elif hasattr(self, 'audio_process'):
                    self.song_modulation('audio_process', 'play')

            if 'restart' in reply.keys():
                if hasattr(self, 'video_process'):
                    self.song_modulation('video_process', 'stop')
                    self.song_modulation('video_process', 'play')
                elif hasattr(self, 'audio_process'):
                    self.song_modulation('audio_process', 'stop')
                    self.song_modulation('audio_process', 'play')

            if 'stop' in reply.keys():
                if hasattr(self, 'video_process'):
                    self.song_modulation('video_process', 'stop')
                elif hasattr(self, 'audio_process'):
                    self.song_modulation('audio_process', 'stop')

                self.transition(self.allowedStateTransitions.get('idle'))

            if 'rss' in reply.keys():
                rss = reply['rss']
                entities = rss['entities']
                count = rss['count']
                for entity in entities[0:count]:
                    logger.debug(entity.title)
                    self.__speak(entity.title)
            self.transition(self.allowedStateTransitions.get('idle'))

        except ConnectionError:
            self.transition(self.allowedStateTransitions.get(
                'error'), payload='ConnectionError')
        except Exception as e:
            logger.error('Got error: %s', e)
            self.transition(self.allowedStateTransitions.get('error'))

    def on_exit(self):
        """Method executed on exit from the Busy State.
        """
        if self.useGPIO:
            try:
                GPIO.output(27, False)
                GPIO.output(22, False)
            except RuntimeError as e:
                logger.error(e)

    def __speak(self, text):
        """Method to set the default TTS for the Speaker
        """
        if self.components.config['default_tts'] == 'google':
            TTS.speak_google_tts(text)
        if self.components.config['default_tts'] == 'flite':
            logger.info("Using flite for TTS")  # indication for using an offline music player
            TTS.speak_flite_tts(text)
        elif self.components.config['default_tts'] == 'watson':
            TTS.speak_watson_tts(text)
