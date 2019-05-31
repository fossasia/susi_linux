""" Play via sound server """

import logging
import requests
from vlcplayer import vlcplayer

baseurl = 'http://localhost:7070/'

def send_request(req):
    try:
        x = requests.get(baseurl + req)
    except Exception as e:
        logger.error(e)

class Player():
    def playytb(self, vid, use_server = True):
        if use_server:
            send_request('play?ytb=' + vid)
        else:
            vlcplayer.playytb(vid)
    def play(self, mrl, use_server = True):
        if use_server:
            send_request('play?mrl=' + mrl)
        else:
            vlcplayer.play(mrl)
    def pause(self, use_server = True):
        if use_server:
            send_request('pause')
        else:
            vlcplayer.pause()
    def resume(self, use_server = True):
        if use_server:
            send_request('resume')
        else:
            vlcplayer.resume()
    def stop(self, use_server = True):
        if use_server:
            send_request('stop')
        else:
            vlcplayer.stop()
    def beep(self, mrl, use_server = True):
        if use_server:
            send_request('beep?mrl=' + mrl)
        else:
            vlcplayer.beep(mrl)
    def say(self, mrl, use_server = True):
        if use_server:
            send_request('say?mrl=' + mrl)
        else:
            vlcplayer.say(mrl)
    def volume(self, val, use_server = True):
        if use_server:
            send_request('volume?val=' + val)
        else:
            vlcplayer.volume(val)
    def save_volume(self, use_server = True):
        if use_server:
            send_request('save_volume')
        else:
            vlcplayer.save_volume()
    def restore_volume(self, use_server = True):
        if use_server:
            send_request('restore_volume')
        else:
            vlcplayer.restore_volume()

player = Player()

