"""Class to represent the Busy State
"""
import os
import signal
import logging

import alsaaudio
import requests
import pafy

from ..speech import TTS
from .base_state import State
from .lights import lights
from ..player import player

try:
    import RPi.GPIO as GPIO
except:
    pass

logger = logging.getLogger(__name__)


class BusyState(State):
    """Busy state inherits from base class State. In this state, SUSI API is called to perform query and the response
    is then spoken with the selected Text to Speech Service.
    """

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
                if classifier[:3] == 'ytd':
                    video_url = reply['identifier']
                    player.playytb(video_url[4:])
                    self.transition(self.allowedStateTransitions.get('idle'))

                else:
                    audio_url = reply['identifier']
                    player.play(audio_url[6:])
                    self.transition(self.allowedStateTransitions.get('idle'))

            if 'volume' in reply.keys():
                player.volume(reply['volume'])
                player.say(os.path.abspath(os.path.join(self.components.config['data_base_dir'],
                                                        self.components.config['detection_bell_sound'])))

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
                player.pause()
                lights.off()
                lights.wakeup()

            if 'resume' in reply.keys():
                player.resume()

            if 'restart' in reply.keys():
                player.restart()    # TODO not implemented!

            if 'stop' in reply.keys():
                player.stop()

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
