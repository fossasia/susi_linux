import os
import sys
import logging
import argparse

import colorlog

from . import SusiLoop
from .player import player


parser = argparse.ArgumentParser(prog='python3 -m susi_linux',
                                 description='SUSI Linux main program')


def get_colorlog_handler(short=False):
    # Short log format is for use under systemd.
    # Here we exclude some info, because they will be added by journalctl.
    if short:
        log_format = '%(log_color)s%(levelname)s:%(reset)s %(message)s'
    else:
        log_format = '%(log_color)s%(asctime)s %(levelname)s:%(name)s:%(reset)s %(message)s'
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.TTYColoredFormatter(
            log_format,
            stream=sys.stderr,
            datefmt='%Y-%m-%d %H:%M:%S'))
    return handler


def startup_sound():
    curr_folder = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(curr_folder, 'wav/ting-ting_susi_has_started.wav')
    player.say(audio_file)


if __name__ == '__main__':

    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Show log. Repeat to get more detailed one.')

    '''
    Sometimes, when we enable -v in systemd service command, and read the log via
    journalctl, we will see duplication of timestamp and process. These info are
    provided by both journalctl and our app. Enable --short-log to stop our app
    from including those info in log.
    '''

    parser.add_argument('--short-log', action='store_true',
                        help='Produce log w/o timestamp and process name.')

    args = parser.parse_args()

    # Configure logger
    if args.verbose:
        levels = (logging.WARNING, logging.INFO, logging.DEBUG)
        handler = get_colorlog_handler(args.short_log)
        lindex = min(args.verbose, len(levels) - 1)
        level = levels[lindex]
        # logging.root.propagate = True
        logging.root.setLevel(level)
        logging.root.handlers = []
        logging.root.addHandler(handler)

    susi_loop = SusiLoop()
    startup_sound()
    susi_loop.start()

