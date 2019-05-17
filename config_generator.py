""" Config Generator script for Susi Hardware. Run this script and input options
 to generate a file for default services for your SUSI Hardware Device
"""
import json_config
import requests
from pathlib import Path
import os
from importlib import util
import sys

config = json_config.connect('config.json')


def is_valid(email, password):
    """ Method to Validate SUSI Login Details
    :param email: SUSI Sign-in email
    :param password: SUSI Sign-in password
    :return: boolean to indicate if details are valid
    """
    print('Checking the validity of login details ....')
    params = {
        'login': email,
        'password': password
    }
    sign_in_url = 'http://api.susi.ai/aaa/login.json?type=access-token'
    api_response = requests.get(sign_in_url, params)
    return [False, True][api_response.status_code == 200]

def setup_wake_button():
    try:
        import RPi.GPIO
        print("\nDevice supports RPi.GPIO")
        # choice = input("Do you wish to enable hardware wake button? (y/n) ")
        choice = sys.argv[4]
        if choice == 'y':
            config['WakeButton'] = 'enabled'
            config['Device'] = 'RaspberryPi'
        else:
            config['WakeButton'] = 'disabled'
    except ImportError:
        print("\nThis device does not support RPi.GPIO")
        config['WakeButton'] = 'not available'
    except RuntimeError:
        print("\nThis device does not support RPi.GPIO")
        config['WakeButton'] = 'not available'


def set_extras():
    """ Method for setting miscellaneous configuration parameters.
    :return: None
    """
    config.setdefault('data_base_dir', os.path.dirname(os.path.abspath(__file__)))
    config.setdefault('flite_speech_file_path', 'extras/cmu_us_slt.flitevox')
    config.setdefault('detection_bell_sound', 'extras/detection-bell.wav')
    config.setdefault('problem_sound', 'extras/problem.wav')
    config.setdefault('recognition_error_sound', 'extras/recognition-error.wav')



def request_hotword_choice():
    """ Method to request user for default Hotword Engine and configure it in settings.
    """
    try:
        print("Checking for Snowboy Availability...")
        snowboy_available = util.find_spec('snowboy')
        found = snowboy_available is not None

    except ImportError:
        print("Some Error Occurred.Snowboy not configured properly.\nUsing PocketSphinx as default engine for Hotword. Run this script again to change")
        found = False
        config['hotword_engine'] = 'PocketSphinx'

    if found is True:
        print("Snowboy is available on this platform")
        # choice = input("Do you wish to use Snowboy as default Hotword Detection Engine (Recommended). (y/n) ")
        choice = sys.argv[3]
        if choice == 'y':
            config['hotword_engine'] = 'Snowboy'
            print('\n Snowboy set as default Hotword Detection Engine \n')
        else:
            config['hotword_engine'] = 'pocket_sphinx'
            print('\n PocketSphinx set as default Hotword Detection Engine \n')
    else:
        print('\n Snowboy not configured Properly\n')
        config['hotword_engine'] = 'pocket_sphinx'
        print('\n PocketSphinx set as default Hotword Detection Engine \n')



def request_stt_choice():
    """ Method for setting default Speech Recognition Service.
    :return: None
    """
    try:
        # choice = int(input('Which Speech Recognition Service do you wish to use? Press number or enter for default.\n'
        #                    '1. Google Voice Recognition (default)\n'
        #                    '2. IBM Watson\n'
        #                    '3. Bing Speech API\n'
        #                    '4. PocketSphinx(offline) \n'))
        choice = sys.argv[1]
        print(choice)
        if choice == 'google':
            config['default_stt'] = 'google'

        elif choice == 'ibm':
            config['default_stt'] = 'watson'
            print('For using IBM Watson. You need API keys for IBM Watson Speech to Text Service'
                  'Please input credentials')
            username = input('Enter Username')
            password = input('Enter Password')
            config['watson_stt_config']['username'] = username
            config['watson_stt_config']['password'] = password
            config['watson_stt_config']['voice'] = 'en-US_AllisonVoice'

        elif choice == 'bing':
            config['default_stt'] = 'bing'
            print('For using Bing Speech API, you need an API key')
            key = input('Enter Bing Speech API Key')
            config['bing_speech_api_key'] = key

        elif choice == 'sphinx':
            config['default_stt'] = 'pocket_sphinx'

        else:
            raise ValueError

    except ValueError:
        print('Invalid Input. Using default Voice Recognition Service')
        config['default_stt'] = 'google'

    print("\nSpeech to Text configured successfully\n")


def request_tts_choice():
    """ Method for setting default Text to Speech Service
    :return: None
    """
    try:
        # choice = int(input('Which Text to Speech Service do you wish to use? Press number or enter for default.\n'
        #                    '1. Google Text to Speech (default)\n'
        #                    '2. Flite TTS (offline)\n'
        #                    '3. IBM Watson\n'))

        choice = sys.argv[2]
        if choice == 'google':
            config['default_tts'] = 'google'

        elif choice == 'flite':
            config['default_tts'] = 'flite'

        elif choice == 'ibm':
            config['default_tts'] = 'watson'
            print('For using IBM Watson. You need API keys for IBM Watson Text to Speech Service'
                  'Please input credentials')
            username = input('Enter Username')
            password = input('Enter Password')
            config['watson_tts_config']['username'] = username
            config['watson_tts_config']['password'] = password
        else:
            raise ValueError

    except ValueError:
        print('Invalid input. Using default Text to Speech Service')
        config['default_tts'] = 'google'

    print("\nSpeech to Text configured successfully\n")


set_extras()

# print(len(sys.argv))

print("Setup Speech to Text Service\n")
request_stt_choice()

print("Setup Text to Speech Service\n")
request_tts_choice()

print("Setup Hotword Detection Engine\n")
request_hotword_choice()

print("Setup Wake Button\n")
setup_wake_button()

print("Run SUSI by 'python3 -m main'")
