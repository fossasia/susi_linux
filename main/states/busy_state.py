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
from ..config import susi_config

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
            no_answer_needed = False

            if isinstance(payload, str):
                logger.debug("Sending payload to susi server: %s", payload)
                reply = self.components.susi.ask(payload)
            else :
                logger.debug("Executing planned action response", payload)
                reply = payload

            if self.useGPIO:
                GPIO.output(27, True)
            if self.components.renderer is not None:
                self.notify_renderer('speaking', payload={'susi_reply': reply})

            if 'plan_delay' in reply.keys() and reply['plan_delay'] != None:
                reply_delay = reply
                ans = reply_delay.pop('answer', None)
                plan_del = reply_delay.pop('plan_delay', None)
                self.components.action_schduler.add_event(int(plan_del)/1000,reply_delay)
                reply={}
                reply['answer']=ans

            #
            # first responses WITHOUT answer key!

            # {'answer': 'Audio volume is now 10 percent.', 'volume': '10'}
            if 'volume' in reply.keys():
                no_answer_needed = True
                player.volume(reply['volume'])
                player.say(os.path.abspath(os.path.join(self.components.config['data_base_dir'],
                                                        self.components.config['detection_bell_sound'])))

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
                if not no_answer_needed and not 'identifier' in reply.keys():
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
                if url[:3] == 'ytd':
                    player.playytb(url[4:])
                else:
                    player.play(url)
                self.transition(self.allowedStateTransitions.get('idle'))

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
