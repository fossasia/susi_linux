from flask import Flask , render_template , request
from flask import jsonify
import subprocess   # nosec #pylint-disable type: ignore
import os
import json_config

access_point_folder = os.path.dirname(os.path.abspath(__file__))
wifi_search_folder = os.path.join(access_point_folder, '..')
config_json_folder = os.path.join(access_point_folder, '../config.json')
configuration_folder = os.path.join(access_point_folder, '../../config_generator.py')
authentication_folder = os.path.join(access_point_folder, '../../authentication.py')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install')
def install():
    return 'starting the installation script'

@app.route('/config', methods=['GET'])
def config():
    stt = request.args.get('stt')
    tts = request.args.get('tts')
    hotword = request.args.get('hotword')
    wake = request.args.get('wake')
    subprocess.Popen(['sudo', 'python3', configuration_folder, stt, tts, hotword, wake])  #nosec #pylint-disable type: ignore
    display_message = {"configuration":"successful", "stt": stt, "tts": tts, "hotword": hotword, "wake":wake}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp # pylint-enable

@app.route('/auth', methods=['GET'])
def login():
    auth = request.args.get('auth')
    email = request.args.get('email')
    password = request.args.get('password')
    subprocess.call(['sudo', 'python3', authentication_folder, auth, email, password]) #nosec #pylint-disable type: ignore
    display_message = {"authentication":"successful", "auth": auth, "email": email, "password": password}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp # pylint-enable

@app.route('/wifi_credentials', methods=['GET'])
def wifi_config():
    wifi_ssid = request.args.get('wifissid')
    wifi_password = request.args.get('wifipassd')
    subprocess.call(['sudo', 'bash', wifi_search_folder + '/wifi_search.sh', wifi_ssid, wifi_password])  #nosec #pylint-disable type: ignore
    display_message = {"wifi":"configured", "wifi_ssid":wifi_ssid, "wifi_password": wifi_password}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp  # pylint-enable

@app.route('/speaker_config', methods=['GET'])
def speaker_config():
    room_name = request.args.get('room_name')
    config = json_config.connect(config_json_folder)
    config['room_name'] = room_name

if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0') #nosec #pylint-disable type: ignore
    # pylint-enable
    # to allow the server to be accessible by any device on the network/access point #pylint-disable type: ignore
