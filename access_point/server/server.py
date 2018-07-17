from flask import Flask , render_template
from flask import jsonify
import subprocess   # nosec #pylint-disable type: ignore
import os

access_point_folder = os.path.dirname(os.path.abspath(__file__))
wifi_search_folder = os.path.join(access_point_folder, '..')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install')
def install():
    return 'starting the installation script'

@app.route('/config/<stt>/<tts>/<hotword>/<wake>')
def config(stt, tts, hotword, wake):
    subprocess.call(['sudo', 'bash' , access_point_folder + '/config.sh', stt, tts, hotword, wake])  #nosec #pylint-disable type: ignore
    display_message = {"Configuration":"Successful"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp # pylint-enable

@app.route('/auth/<auth>/<email>/<passwd>')
def login(auth, email, passwd):
    subprocess.call(['sudo', 'bash', access_point_folder + '/login.sh', auth, email, passwd]) #nosec #pylint-disable type: ignore
    display_message = {"Authentication":"Successful"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp # pylint-enable

@app.route('/wifi_credentials/<wifissid>/<wifipassd>')
def wifi_config(wifissid,wifipassd):
    wifi_ssid = wifissid
    wifi_password = wifipassd
    subprocess.call(['sudo', 'bash', wifi_search_folder + '/wifi_search.sh', wifi_ssid, wifi_password])  #nosec #pylint-disable type: ignore
    display_message = {"Wifi":"Configured"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp  # pylint-enable


if __name__ == '__main__':
    app.run(debug=False,host= '0.0.0.0') #nosec #pylint-disable type: ignore
    # pylint-enable
    # to allow the server to be accessible by any device on the network/access point #pylint-disable type: ignore
