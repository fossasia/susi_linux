from main import SusiStateMachine
import json_config
import subprocess  # nosec #pylint-disable type: ignore
import os

config = json_config.connect('config.json')
curr_folder = os.path.dirname(os.path.abspath(__file__))


def startup_sound():
    audio_file = os.path.join(curr_folder, 'wav/ting-ting_susi_has_started.wav')
    subprocess.Popen(['play', audio_file])  # nosec #pylint-disable type: ignore


if __name__ == '__main__':
    startup_sound()
    susiStateMachine = SusiStateMachine()
    susiStateMachine.start()
