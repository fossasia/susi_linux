""" Config Generator script for Susi Hardware. Run this script and input options
 to generate a file for default services for your SUSI Hardware Device
"""
import json_config

config = json_config.connect('config.json')


def set_extras():
    """ Method for setting miscellaneous configuration parameters.
    :return: None
    """
    config['flite_speech_file_path'] = 'extras/cmu_us_slt.flitevox'
    config['detection_bell_sound'] = 'extras/detection-bell.wav'


def request_stt_choice():
    """ Method for setting default Speech Recognition Service.
    :return: None
    """
    try:
        choice = int(input('Which Speech Recognition Service do you wish to use? Press number or enter for default.\n'
                           '1. Google Voice Recognition (default)\n'
                           '2. IBM Watson\n'
                           '3. Bing Speech API\n'))
        if choice == 1:
            config['default_stt'] = 'google'

        elif choice == 2:
            config['default_stt'] = 'watson'
            print('For using IBM Watson. You need API keys for IBM Watson Speech to Text Service'
                  'Please input credentials')
            username = input('Enter Username')
            password = input('Enter Password')
            config['watson_stt_config']['username'] = username
            config['watson_stt_config']['password'] = password
            config['watson_stt_config']['voice'] = 'en-US_AllisonVoice'

        elif choice == 3:
            config['default_stt'] = 'bing'
            print('For using Bing Speech API, you need an API key')
            key = input('Enter Bing Speech API Key')
            config['bing_speech_api_key'] = key

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
        choice = int(input('Which Text to Speech Service do you wish to use? Press number or enter for default.\n'
                           '1. Google Text to Speech (default)\n'
                           '2. Flite TTS (offline)\n'
                           '3. IBM Watson\n'))
        if choice == 1:
            config['default_tts'] = 'google'

        elif choice == 2:
            config['default_tts'] = 'flite'

        elif choice == 3:
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

print("Setup Speech to Text Service")
request_stt_choice()

print("Setup Text to Speech Service")
request_tts_choice()
