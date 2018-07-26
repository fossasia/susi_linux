from main import SusiStateMachine
import json_config
import susi_python as susi

config = json_config.connect('config.json')

def add_device():
    susi.sign_in(config['login_credentials']['email'], config['login_credentials']['password'], speaker_name = config['speaker_name'], room_name = config['room_name'])


if __name__ == '__main__':
    add_device()
    susiStateMachine = SusiStateMachine()
    susiStateMachine.start()
