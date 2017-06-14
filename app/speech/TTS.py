import subprocess
import wave
from os.path import join, dirname

import pyaudio
from watson_developer_cloud import TextToSpeechV1


class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()


text_to_speech = TextToSpeechV1(
    username='ADD_API_USERNAME_HERE',
    password='ADD_API_PASSWORD HERE',
    x_watson_learning_opt_out=True)  # Optional flag


def speak_flite_tts(text):
    filename = '.response'
    file = open(filename, 'w')
    file.write(text)
    file.close()
    # Call flite tts to reply the response by Susi
    subprocess.call('flite -voice file://cmu_us_slt.flitevox -f ' + filename, shell=True)


def speak_watson_tts(text):

    with open(join(dirname(__file__), 'output.wav'),
              'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept='audio/wav',
                                      voice="en-US_AllisonVoice"))

    a = AudioFile("speech/output.wav")
    a.play()
    a.close()
