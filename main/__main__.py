from main import SusiStateMachine
import json_config
import susi_python as susi
import subprocess
import os

config = json_config.connect('config.json')
curr_folder = os.path.dirname(os.path.abspath(__file__))

def add_device():
    susi.sign_in(config['login_credentials']['email'], config['login_credentials']['password'], room_name=config['room_name'])

def startup_sound():
    audio_file = os.path.join(curr_folder,'wav/ting-ting_susi_has_started.wav')
    subprocess.Popen(['play',audio_file])

if __name__ == '__main__':
    add_device()
    startup_sound()
    susiStateMachine = SusiStateMachine()
    susiStateMachine.start()
