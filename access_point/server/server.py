from flask import Flask , render_template
import subprocess   # nosec #pylint-disable type: ignore
import os

access_point_folder = os.path.dirname(os.path.abspath(__file__))
server_folder = os.path.join(access_point_folder, 'server')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install')
def install():
    return 'starting the installation script'

@app.route('/config/<stt>/<tts>/<hotword>/<wake>')
def config(stt, tts, hotword, wake):
    subprocess.call(['sudo', 'bash' , server_folder + '/config.sh', stt, tts, hotword, wake])  #nosec #pylint-disable type: ignore
    return 'Done' # pylint-enable

@app.route('/auth/<auth>/<email>/<passwd>')
def login(auth, email, passwd):
    subprocess.call(['sudo', 'bash', server_folder + '/login.sh', auth, email, passwd]) #nosec #pylint-disable type: ignore
    return 'Authenticated' # pylint-enable

@app.route('/wifi_credentials/<wifissid>/<wifipassd>')
def wifi_config(wifissid,wifipassd):
    wifi_ssid = wifissid
    wifi_password = wifipassd
    subprocess.call(['sudo', 'bash', access_point_folder + '/wifi_search.sh', wifi_ssid, wifi_password])  #nosec #pylint-disable type: ignore
    return 'Wifi Configured' # pylint-enable

if __name__ == '__main__':
    app.run(debug=False,host= '0.0.0.0') #nosec #pylint-disable type: ignore
    # pylint-enable
    # to allow the server to be accessible by any device on the network/access point #pylint-disable type: ignore
