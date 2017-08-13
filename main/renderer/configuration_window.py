import os

import gi
import json_config

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file(os.path.join(TOP_DIR, "glade_files/configure.glade"))

window = builder.get_object("configuration_window")


class Handler():
    def on_delete_window(self, *args):
        print('Exiting')
        Gtk.main_quit(*args)

    def on_stt_cb_changed(self):
        selection = STT_COMBOBOX.get_active_text()
        if selection == 'google':
            config['default_stt'] = 'google'
        elif selection == 'watson':
            pass

    def on_tts_cb_changed(self):
        pass

def init_combobox():
    default_stt = config['default_stt']
    if default_stt == 'google':
        STT_COMBOBOX.set_active(0)
    elif default_stt == 'watson':
        STT_COMBOBOX.set_active(1)
    elif default_stt == 'bing':
        STT_COMBOBOX.set_active(2)


STT_COMBOBOX = builder.get_object("stt_combobox")
TTS_COMBOBOX = builder.get_object("tts_combobox")
AUTH_SWITCH = builder.get_object("auth_switch")
SNOWBOY_SWITCH = builder.get_object("snowboy_switch")
WAKE_BUTTON_SWITCH = builder.get_object("wake_button_switch")
init_combobox()

builder.connect_signals(Handler())
window.set_resizable(False)
window.show_all()

Gtk.main()
