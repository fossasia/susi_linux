""" Play via sound server """

import logging
import requests

baseurl = 'http://localhost:7070/'

def send_request(req):
    try:
        x = requests.get(baseurl + req)
    except Exception as e:
        logger.error(e)


class Player():
    def playytb(self, vid):
        send_request('play?ytb=' + vid)
    def play(self, mrl):
        send_request('play?mrl=' + mrl)
    def pause(self):
        send_request('pause')
    def resume(self):
        send_request('resume')
    def stop(self):
        send_request('stop')
    def beep(self, mrl):
        send_request('beep?mrl=' + mrl)
    def say(self, mrl):
        send_request('say?mrl=' + mrl)
    def volume(self, val):
        send_request('volume?val=' + val)
    def save_volume(self):
        send_request('save_volume')
    def restore_volume(self):
        send_request('restore_volume')

player = Player()

