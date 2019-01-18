from flask import Flask , render_template , request
from flask import jsonify
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
    display_message = {"song": "started", "url": playurl}
    resp = jsonify(display_message)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=False, port=7070, host='0.0.0.0')
