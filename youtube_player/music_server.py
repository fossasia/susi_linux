from flask import Flask , render_template , request
from flask import jsonify
import subprocess   # nosec #pylint-disable type: ignore
import os
import json_config
import pafy
import vlc

app = Flask(__name__)
Instance = vlc.Instance('--no-video')
player = Instance.media_player_new()
url = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/song', methods=['GET'])
def youtube():
    vid = request.args.get('vid')
    url = 'https://www.youtube.com/watch?v=' + vid
    video = pafy.new(url)
    streams = video.audiostreams
    best = streams[3]
    playurl = best.url
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    display_message = {"song":"started"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

@app.route('/pause')
def pause():
    player.pause()
    display_message = {"song":"paused"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

@app.route('/stop')
def stop():
    player.stop()
    display_message = {"song":"stopped"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

@app.route('/restart')
def restart():
    player.stop()
    player.player()
    display_message = {"song":"restarted"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

@app.route('/resume')
def play():
    player.play()
    display_message = {"song":"played"}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    app.run(debug=True,port=7070,host= '0.0.0.0')
