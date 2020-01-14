""" This module implements all Text to Speech Services.
You may use any of the speech synthesis services by calling the
respective method.
"""
import logging
import os
import subprocess   # nosec #pylint-disable type: ignore
import tempfile
from google_speech import Speech
from watson_developer_cloud import TextToSpeechV1
from ..player import player
from susi_config import SusiConfig

logger = logging.getLogger(__name__)
susicfg = SusiConfig()

text_to_speech = TextToSpeechV1(
    username=susicfg.config['watson_tts_config']['username'],
    password=susicfg.config['watson_tts_config']['password'])


def speak_flite_tts(text):
    """ This method implements Text to Speech using the Flite TTS.
    Flite TTS is completely offline. Usage of Flite is recommended if
    good internet connection is not available"
    :param text: Text which is needed to be spoken
    :return: None
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        fd, filename = tempfile.mkstemp(text=True, dir=tmpdirname)
        with open(fd, 'w') as f:
            f.write(text)
        # Call flite tts to reply the response by Susi
        flite_speech_file = os.path.join(
            susicfg.config['data_base_dir'], susicfg.config['flite_speech_file_path'])
        logger.debug(
            'flite -voice file://%s -f %s', flite_speech_file, filename)
        fdout, wav_output = tempfile.mkstemp(suffix='.wav', dir=tmpdirname)
        subprocess.call(   # nosec #pylint-disable type: ignore
            ['flite', '-v', '-voice', 'file://' + flite_speech_file, '-f', filename, '-o', wav_output])   # nosec #pylint-disable type: ignore
        player.say(wav_output)


def speak_watson_tts(text):
    """ This method implements Text to Speech using the IBM Watson TTS.
    To use this, set username and password parameters in config file.
    :param text: Text which is needed to be spoken
    :return: None
    """
    if "voice" in susicfg.config['watson_tts_config']:
        voice = susicfg.config['watson_tts_config']['voice']
    elif susicfg.config["language"][0:2] == "en":
        voice = "en-US_AllisonVoice"
    elif susicfg.config["language"][0:2] == "de":
        voice = "de-DE_BirgitVoice"
    elif susicfg.config["language"][0:2] == "es":
        voice = "es-ES_LauraVoice"
    elif susicfg.config["language"][0:2] == "fr":
        voice = "fr-FR_ReneeVoice"
    elif susicfg.config["language"][0:2] == "it":
        voice = "it-IT_FrancescaVoice"
    elif susicfg.config["language"][0:2] == "ja":
        voice = "ja-JP_EmiVoice"
    elif susicfg.config["language"][0:2] == "pt":
        voice = "pt-BR_IsabelaVoice"
    else:
        # switch to English as default
        voice = "en-US_AllisonVoice"

    with tempfile.TemporaryDirectory() as tmpdirname:
        fd, wav_output = tempfile.mkstemp(suffix='.wav', dir=tmpdirname)
        with open(fd, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(text, accept='audio/wav', voice=voice))

        player.say(wav_output)


def speak_google_tts(text):
    """ This method implements Text to Speech using the Google Translate TTS.
    It uses Google Speech Python Package.
    :param text: Text which is needed to be spoken
    :return: None
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        fd, mpiii = tempfile.mkstemp(suffix='.mp3', dir=tmpdirname)
        Speech(text=text, lang=susicfg.config["language"]).save(mpiii)
        player.say(mpiii)

    # sox_effects = ("tempo", "1.2", "pitch", "2", "speed", "1")
    # player.save_softvolume()
    # player.volume(20)
    # Speech(text=text, lang='en').play(sox_effects)
    # player.restore_volume()
