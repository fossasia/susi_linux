import subprocess
from utils.audio_utils import AudioFile
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

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
    subprocess.call('flite -voice file://extras/cmu_us_slt.flitevox -f ' + filename, shell=True)


def speak_watson_tts(text):

    with open('extras/output.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept='audio/wav',
                                      voice="en-US_AllisonVoice"))

    a = AudioFile("extra/output.wav")
    a.play()
    a.close()
