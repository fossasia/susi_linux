"""Class to represent the Busy State
"""
from ..speech import TTS
from .base_state import State
import subprocess   # nosec #pylint-disable type: ignore
import alsaaudio
from .lights import lights
import os
from ..hotword_engine.stop_detection import StopDetector
import signal


class BusyState(State):
    """Busy state inherits from base class State. In this state, SUSI API is called to perform query and the response
    is then spoken with the selected Text to Speech Service.
    """
    def detection(self):
        """This callback is fired when a Hotword Detector detects a hotword.
        :return: None
        """
        # subprocess.call(['killall', 'play'])
        # subprocess.call(['killall', 'mpv']
        if 'vid_pid' in self.__dict__:
            self.video_pid.send_signal(signal.SIGSTOP)  # nosec #pylint-disable type: ignore
            lights.wakeup()
            subprocess.Popen(['play', str(self.components.config['detection_bell_sound'])])  # nosec #pylint-disable type: ignore
            lights.off()
            self.transition(self.allowedStateTransitions.get('recognizing'))
            self.video_pid.send_signal(signal.SIGCONT)  # nosec #pylint-disable type: ignore
        if 'audio_pid' in self.__dict__:
            self.audio_pid.send_signal(signal.SIGSTOP)  # nosec #pylint-disable type: ignore
            lights.wakeup()
            subprocess.Popen(['play', str(self.components.config['detection_bell_sound'])])  # nosec #pylint-disable type: ignore
            lights.wakeup()
            self.transition(self.allowedStateTransitions.get('recognizing'))
            self.audio_pid.send_signal(signal.SIGCONT)  # nosec #pylint-disable type: ignore

    def on_enter(self, payload=None):
        """This method is executed on entry to Busy State. SUSI API is called via SUSI Python library to fetch the
        result. We then call TTS to speak the reply. If successful, we transition to Idle State else to the Error State.
        :param payload: query to be asked to SUSI
        :return: None
        """
        print('busy')
        try:
            import RPi.GPIO as GPIO
            GPIO.output(17, True)
            reply = self.components.susi.ask(payload)
            GPIO.output(17, False)
            GPIO.output(27, True)
            if self.components.renderer is not None:
                self.notify_renderer('speaking', payload={'susi_reply': reply})

            if 'answer' in reply.keys():
                print('Susi:' + reply['answer'])
                lights.speak()
                self.__speak(reply['answer'])
                lights.off()
            else:
                lights.speak()
                self.__speak("I don't have an answer to this")
                lights.off()

            if 'identifier' in reply.keys():
                classifier = reply['identifier']
                stopAction = StopDetector(self.detection)
                if classifier[:3] == 'ytd':
                    video_url = reply['identifier']
                    video_pid = subprocess.Popen(['mpv', '--no-video', 'https://www.youtube.com/watch?v=' + video_url[4:] , '--really-quiet'])  # nosec #pylint-disable type: ignore
                    self.video_pid = video_pid
                    stopAction.run()
                    stopAction.detector.terminate()
                else:
                    audio_url = reply['identifier']
                    audio_pid = subprocess.Popen(['play', audio_url[6:] , '--no-show-progress'])  # nosec #pylint-disable type: ignore
                    self.audio_pid = audio_pid
                    stopAction.run()
                    stopAction.detector.terminate()

            if 'volume' in reply.keys():
                m = alsaaudio.Mixer()
                m.setvolume(int(reply['volume']))
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

            if 'stop' in reply.keys():
                subprocess.call(['killall', 'mpv'])  # nosec #pylint-disable type: ignore
                subprocess.call(['killall', 'play'])  # nosec #pylint-disable type: ignore
                self.transition(self.allowedStateTransitions.get('idle'))

            if 'rss' in reply.keys():
                rss = reply['rss']
                entities = rss['entities']
                count = rss['count']
                for entity in entities[0:count]:
                    print(entity.title)
                    self.__speak(entity.title)
            print('TMKC')
            self.transition(self.allowedStateTransitions.get('idle'))

        except ConnectionError:
            self.transition(self.allowedStateTransitions.get(
                'error'), payload='ConnectionError')
        except Exception as e:
            print(e)
            self.transition(self.allowedStateTransitions.get('error'))

    def on_exit(self):
        """Method executed on exit from the Busy State.
        """
        try:
            import RPi.GPIO as GPIO
            GPIO.output(17, False)
            GPIO.output(27, False)
            GPIO.output(22, False)
            pass
        except RuntimeError:
            pass
        except ImportError:
            print("Only available for devices with RPI.GPIo ports")

    def __speak(self, text):
        if self.components.config['default_tts'] == 'google':
            TTS.speak_google_tts(text)
        if self.components.config['default_tts'] == 'flite':
            print("Using flite for TTS")
            TTS.speak_flite_tts(text)
        elif self.components.config['default_tts'] == 'watson':
            TTS.speak_watson_tts(text)
