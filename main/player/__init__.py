""" Play via sound server """

import logging
import requests
from vlcplayer import vlcplayer

logger = logging.getLogger(__name__)
default_mode = 'server'
baseurl = 'http://localhost:7070/'

def send_request(req):
    try:
        requests.get(baseurl + req)
    except Exception as e:
        logger.error(e)

class Player():
    def __init__(self, mode = None):
        if mode is None:
            mode = default_mode
        if (not mode == 'server') and (not mode == 'direct'):
            logger.error('unknown mode %s, trying default mode', mode)
            mode = default_mode
        if mode == 'server':
            # try to check whether server is available
            try:
                requests.get(baseurl + 'status')
                self.mode = 'server'
            except Exception:
                self.mode = 'direct'
                logger.info('sound server not available, switching to direct play mode')
        else:
            self.mode = 'direct'
        logger.info('Player is working in mode: %s', self.mode)

    def playytb(self, vid, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('play?ytb=' + vid)
        else:
            vlcplayer.playytb(vid)
    def play(self, mrl, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('play?mrl=' + mrl)
        else:
            vlcplayer.play(mrl)
    def pause(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('pause')
        else:
            vlcplayer.pause()
    def resume(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('resume')
        else:
            vlcplayer.resume()
    def next(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('next')
        else:
            vlcplayer.next()
    def previous(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('previous')
        else:
            vlcplayer.previous()
    def restart(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('restart')
        else:
            vlcplayer.restart()
    def stop(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('stop')
        else:
            vlcplayer.stop()
    def beep(self, mrl, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('beep?mrl=' + mrl)
        else:
            vlcplayer.beep(mrl)
    def say(self, mrl, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('say?mrl=' + mrl)
        else:
            vlcplayer.say(mrl)
    def volume(self, val, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('volume?val=' + str(val))
        else:
            vlcplayer.volume(val)
    def save_softvolume(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('save_softvolume')
        else:
            vlcplayer.save_softvolume()
    def restore_softvolume(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('restore_softvolume')
        else:
            vlcplayer.restore_softvolume()
    def save_hardvolume(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('save_hardvolume')
        else:
            vlcplayer.save_hardvolume()
    def restore_hardvolume(self, mode = None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('restore_hardvolume')
        else:
            vlcplayer.restore_hardvolume()


player = Player()
