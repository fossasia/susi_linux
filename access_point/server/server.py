""" This script creates a light flask server to allow the Smart Speaker to connect with the external clients.
The endpoints will be hit through the mobile clients in the following order (SYNCHRONOUSLY):

1.Room Name
2.Wifi Credentials
3.Authentication
4. Configuration (/config)
"""

from flask import Flask , render_template , request , jsonify
import subprocess   # nosec #pylint-disable type: ignore
import os
import json_config

access_point_folder = os.path.dirname(os.path.abspath(__file__))
wifi_search_folder = os.path.join(access_point_folder, '..')
config_json_folder = os.path.join(access_point_folder, '../../')
config_json_file  = os.path.join(access_point_folder, '../../config.json')
configuration_script =  os.path.join(access_point_folder, '../../config_generator.py')
authentication_script =  os.path.join(access_point_folder, '../../authentication.py')

app = Flask(__name__, static_folder="static")

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
    os.chdir(config_json_folder)
    subprocess.Popen(['sudo', 'python3', configuration_script, stt, tts, hotword, wake])  #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'daemon-reload']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'disable', 'ss-python-flask.service']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'enable', 'ss-susi-linux.service']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'enable', 'ss-factory-daemon.service']) #nosec #pylint-disable type: ignore
    display_message = {"configuration":"successful", "stt": stt, "tts": tts, "hotword": hotword, "wake":wake}
    resp = jsonify(display_message)
    resp.status_code = 200
    subprocess.Popen(['sudo','bash',os.path.join(wifi_search_folder,'rwap.sh')])
    return resp # pylint-enable

@app.route('/auth', methods=['GET'])
def login():
    auth = request.args.get('auth')
    email = request.args.get('email')
    password = request.args.get('password')
    os.chdir(config_json_folder)
    subprocess.call(['sudo', 'python3', authentication_script, auth, email, password]) #nosec #pylint-disable type: ignore
    display_message = {"authentication":"successful", "auth": auth, "email": email, "password": password}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp # pylint-enable

@app.route('/wifi_credentials', methods=['GET'])
def wifi_config():
    wifi_ssid = request.args.get('wifissid')
    wifi_password = request.args.get('wifipassd')
    os.chdir(config_json_folder)
    subprocess.call(['sudo', 'bash', wifi_search_folder + '/wifi_search.sh', wifi_ssid, wifi_password])  #nosec #pylint-disable type: ignore
    display_message = {"wifi":"configured", "wifi_ssid":wifi_ssid, "wifi_password": wifi_password}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp  # pylint-enable

@app.route('/speaker_config', methods=['GET'])
def speaker_config():
    room_name = request.args.get('room_name')
    config = json_config.connect(config_json_file)
    config['room_name'] = room_name
    display_message = {"room_name":room_name}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

# the reboot service combines all other services in one call
# the current version allows anonymous operation mode
# todo: the front-end should provide an option for this

@app.route('/reboot', methods=['POST'])
def reboot():
    config = json_config.connect(config_json_file)

    # speaker_config
    room_name = request.form['room_name'] 
    config['room_name'] = room_name

    # wifi_credentials
    wifi_ssid = request.form['wifissid']
    wifi_password = request.form['wifipassd']
    os.chdir(config_json_folder)
    subprocess.call(['sudo', 'bash', wifi_search_folder + '/wifi_search.sh', wifi_ssid, wifi_password])  #nosec #pylint-disable type: ignore

    # auth
    auth = request.form['auth']
    email = request.form['email']
    password = request.form['password']

    # config
    stt = request.form['stt']
    tts = request.form['tts']
    hotword = request.form['hotword']
    wake = request.form['wake']
    subprocess.Popen(['sudo', 'python3', configuration_script, stt, tts, hotword, wake])  #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'daemon-reload']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'disable', 'ss-python-flask.service']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'enable', 'ss-susi-linux.service']) #nosec #pylint-disable type: ignore
    subprocess.call(['sudo', 'systemctl', 'enable', 'ss-factory-daemon.service']) #nosec #pylint-disable type: ignore
    subprocess.Popen(['sudo','bash',os.path.join(wifi_search_folder,'rwap.sh')])
    display_message = {"wifi":"configured", "room_name":room_name, "wifi_ssid":wifi_ssid, "auth":auth, "email":email, "stt":stt, "tts":tts, "hotword":hotword, "wake":wake, "message":"SUSI is rebooting"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp  # pylint-enable

if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0') #nosec #pylint-disable type: ignore
    # pylint-enable
    # to allow the server to be accessible by any device on the network/access point #pylint-disable type: ignore
