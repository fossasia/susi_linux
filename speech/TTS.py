import subprocess
import os

from watson_developer_cloud import TextToSpeechV1

from utils.audio_utils import AudioFile
from utils.susi_config import config

text_to_speech = TextToSpeechV1(
    username=config['watson_tts_config']['username'],
    password=config['watson_tts_config']['password'])


def speak_flite_tts(text):
    filename = '.response'
    file = open(filename, 'w')
    file.write(text)
    file.close()
    # Call flite tts to reply the response by Susi
    flite_speech_file = config['flite_speech_file_path']
    print('flite -voice file://{0} -f {1}'.format(flite_speech_file, filename))
    os.system('flite -v -voice file://{0} -f {1} -o extras/output.wav'.format(flite_speech_file, filename))
    os.system('play extras/output.wav')

def speak_watson_tts(text):
    with open('extras/output.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept='audio/wav',
                                      voice=config['watson_tts_config']['voice']))

    a = AudioFile("extras/output.wav")
    a.play()
