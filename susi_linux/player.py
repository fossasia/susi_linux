""" Play via sound server """

import logging
import requests
from vlcplayer import vlcplayer

logger = logging.getLogger(__name__)
default_mode = 'server'
baseurl = 'http://localhost:7070/'


def send_request(req):
    try:
        requests.post(baseurl + req)
    except Exception as e:
        logger.error(e)


class Player():

    def __init__(self, mode=None):
        if mode is None:
            mode = default_mode
        if (not mode == 'server') and (not mode == 'direct'):
            logger.error('unknown mode %s, trying default mode', mode)
            mode = default_mode
        if mode == 'server':
            # try to check whether server is available
            try:
                requests.post(baseurl + 'status')
                self.mode = 'server'
            except Exception:
                self.mode = 'direct'
                logger.info('sound server not available, switching to direct play mode')
        else:
            self.mode = 'direct'
        logger.info('Player is working in mode: %s', self.mode)

    def _execute(self, method, mode=None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request(method)
        else:
            getattr(vlcplayer, method)()

    def _executeArg(self, method, key, arg, mode=None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request(method + '?' + key + '=' + arg)
        else:
            getattr(vlcplayer, method)(arg)

    def playytb(self, vid, mode=None):
        if (mode == 'server') or ((mode is None) and (self.mode == 'server')):
            send_request('play?ytb=' + vid)
        else:
            vlcplayer.playytb(vid)

    def play(self, mrl, mode=None):
        self._executeArg('play', 'mrl', mrl, mode)

    def pause(self, mode=None):
        self._execute('pause', mode)

    def resume(self, mode=None):
        self._execute('resume', mode)

    def next(self, mode=None):
        self._execute('next', mode)

    def previous(self, mode=None):
        self._execute('previous', mode)

    def restart(self, mode=None):
        self._execute('restart', mode)

    def stop(self, mode=None):
        self._execute('stop', mode)

    def beep(self, mrl, mode=None):
        self._executeArg('beep', 'mrl', mrl, mode)

    def say(self, mrl, mode=None):
        self._executeArg('say', 'mrl', mrl, mode)

    def shuffle(self, mode=None):
        self._execute('shuffle', mode)

    def volume(self, val, mode=None):
        self._executeArg('volume', 'val', val, mode)

    def save_softvolume(self, mode=None):
        self._execute('save_softvolume', mode)

    def restore_softvolume(self, mode=None):
        self._execute('restore_softvolume', mode)

    def save_hardvolume(self, mode=None):
        self._execute('save_hardvolume', mode)

    def restore_hardvolume(self, mode=None):
        self._execute('restore_hardvolume', mode)


player = Player()
