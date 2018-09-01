import json_config

import susi_python as susi


if __name__ == '__main__':
    config = json_config.connect('config.json')
    susi.sign_in(config['login_credentials']['email'], config['login_credentials']['password'], room_name=config['room_name'])
