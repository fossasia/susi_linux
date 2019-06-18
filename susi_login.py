import json_config

from susi_python import susi_client as susi


if __name__ == '__main__':
    config = json_config.connect('config.json')
    susi.sign_in(config['login_credentials']['email'], config['login_credentials']['password'], room_name=config['room_name'])
