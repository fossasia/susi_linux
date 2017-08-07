import speech_recognition as sr

import speech.TTS as TTS
import susi_python as susi
from utils import websocket_utils
from utils.susi_config import config

from queue import Queue

callback_queue = Queue(1)

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 2000

microphone = sr.Microphone()
wake_button = None


# Websocket Callbacks
def on_new_client(client, server):
    # server.send_message_to_all("Hey all, a new client has joined us")
    pass


def on_client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


def on_message_received(client, server, message):
    # speak(message)
    reply = susi.answer_from_json(message)

    if 'answer' in reply.keys():
        print('Susi:' + reply['answer'])
        # Call flite tts to reply the response by Susi
        speak(reply['answer'])


websocketThread = websocket_utils.WebsocketThread(
    port=9001,
    fn_message_received=on_message_received,
    fn_client_left=on_client_left,
    fn_new_client=on_new_client
)


def speak(text):
    if config['default_tts'] == 'google':
        TTS.speak_google_tts(text)
    if config['default_tts'] == 'flite':
        TTS.speak_flite_tts(text)
    elif config['default_tts'] == 'watson':
        TTS.speak_watson_tts(text)


def ask_susi(input_query):
    # get reply by Susi
    reply = susi.ask(input_query)

    if 'answer' in reply.keys():
        print('Susi:' + reply['answer'])
        # Call festival tts to reply the response by Susi
        speak(reply['answer'])
    else:
        speak("I don't have an answer to this")


def recognize_audio(audio):
    if config['default_stt'] == 'google':
        return recognizer.recognize_google(audio)

    elif config['default_stt'] == 'watson':
        username = config['watson_stt_config']['username']
        password = config['watson_stt_config']['password']
        return recognizer.recognize_ibm(
            username=username,
            password=password,
            audio_data=audio)


def start_speech_recognition():
    try:
        print("Say something!")
        with microphone as source:
            audio = recognizer.listen(source, phrase_time_limit=5)
        print("Got it! Now to recognize it...")
        try:
            value = recognize_audio(audio)
            # websocketThread.send_to_all(value)
            print(value)
            ask_susi(value)
            hotword_detector.start_detection()
            if wake_button is not None:
                wake_button.is_active = True

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            hotword_detector.start_detection()
            if wake_button is not None:
                wake_button.is_active = True
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            hotword_detector.start_detection()
            if wake_button is not None:
                wake_button.is_active = True

    except KeyboardInterrupt:
        pass


# websocketThread.start()

if config['usage_mode'] == 'authenticated':
    try:
        susi.sign_in(email=config['login_credentials']['email'],
                     password=config['login_credentials']['password'])
    except Exception:
        print('Some error occurred in login. Check you login details in config.json')

hotword_detector = None

""" Check the Hotword Engine selected as default and import it.
"""
if config['hotword_engine'] == 'Snowboy':
    from hotword_engine import SnowboyDetector

    hotword_detector = SnowboyDetector(callback_queue, detection_callback=start_speech_recognition)
else:
    from hotword_engine import PocketSphinxDetector

    hotword_detector = PocketSphinxDetector(callback_queue, detection_callback=start_speech_recognition)

if config['wake_button'] == 'enabled':
    if config['device'] == 'RaspberryPi':
        from hardware_components import RaspberryPiWakeButton

        wake_button = RaspberryPiWakeButton(callback_queue=callback_queue, detection_callback=start_speech_recognition)
        wake_button.start()
        wake_button.is_active = True

hotword_detector.start()
hotword_detector.start_detection()

while True:
    func = callback_queue.get()
    func()

# websocketThread.join()
