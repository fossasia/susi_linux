import os

import gi
import json_config
import login_screen

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file(os.path.join(TOP_DIR, "glade_files/configure.glade"))

window = builder.get_object("configuration_window")


class WatsonCredentialsDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Enter Credentials", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        username_field = Gtk.Entry()
        username_field.set_placeholder_text("Username")
        password_field = Gtk.Entry()
        password_field.set_placeholder_text("Password")
        password_field.set_visibility(False)
        password_field.set_invisible_char('*')

        self.username_field = username_field
        self.password_field = password_field

        box = self.get_content_area()

        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_left(10)
        box.set_margin_right(10)

        box.set_spacing(10)

        box.add(username_field)
        box.add(password_field)
        self.show_all()


class BingCredentialDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Enter API Key", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        api_key_field = Gtk.Entry()
        api_key_field.set_placeholder_text("API Key")

        self.api_key_field = api_key_field

        box = self.get_content_area()

        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_left(10)
        box.set_margin_right(10)

        box.set_spacing(10)

        box.add(api_key_field)
        self.show_all()


class Handler():
    def on_delete_window(self, *args):
        print('Exiting')
        Gtk.main_quit(*args)

    def on_stt_combobox_changed(self, combo: Gtk.ComboBox):
        selection = combo.get_active()

        if selection == 0:
            config['default_stt'] = 'google'

        elif selection == 1:
            credential_dialog = WatsonCredentialsDialog(window)
            response = credential_dialog.run()

            if response == Gtk.ResponseType.OK:
                username = credential_dialog.username_field.get_text()
                password = credential_dialog.password_field.get_text()
                config['default_stt'] = 'watson'
                config['watson_stt_config']['username'] = username
                config['watson_stt_config']['password'] = password
            else:
                init_stt_combobox()

            credential_dialog.destroy()

        elif selection == 2:
            credential_dialog = BingCredentialDialog(window)
            response = credential_dialog.run()

            if response == Gtk.ResponseType.OK:
                api_key = credential_dialog.api_key_field.get_text()
                config['default_stt'] = 'bing'
                config['bing_speech_api_key']['username'] = api_key
            else:
                init_stt_combobox()

            credential_dialog.destroy()

    def on_tts_combobox_changed(self, combo):
        selection = combo.get_active()

        if selection == 0:
            config['default_tts'] = 'google'

        elif selection == 1:
            config['default_tts'] = 'flite'

        elif selection == 2:
            credential_dialog = WatsonCredentialsDialog(window)
            response = credential_dialog.run()

            if response == Gtk.ResponseType.OK:
                username = credential_dialog.username_field.get_text()
                password = credential_dialog.password_field.get_text()
                config['default_tts'] = 'watson'
                config['watson_tts_config']['username'] = username
                config['watson_tts_config']['password'] = password
                config['watson_tts_config']['voice'] = 'en-US_AllisonVoice'
            else:
                init_tts_combobox()
            credential_dialog.destroy()

    def on_auth_switch_active_notify(self, switch, gparam):
        if switch.get_active():
            login_screen.main()
            if config['usage_mode'] == 'authenticated':
                switch.set_active(True)
            else:
                switch.set_active(False)


def init_tts_combobox():
    default_tts = config['default_tts']
    if default_tts == 'google':
        TTS_COMBOBOX.set_active(0)
    elif default_tts == 'flite':
        TTS_COMBOBOX.set_active(1)
    elif default_tts == 'watson':
        TTS_COMBOBOX.set_active(2)
    else:
        TTS_COMBOBOX.set_active(0)
        config['default_tts'] = 'google'


def init_stt_combobox():
    default_stt = config['default_stt']
    if default_stt == 'google':
        STT_COMBOBOX.set_active(0)
    elif default_stt == 'watson':
        STT_COMBOBOX.set_active(1)
    elif default_stt == 'bing':
        STT_COMBOBOX.set_active(2)
    else:
        TTS_COMBOBOX.set_active(0)
        config['default_tts'] = 'google'


def init_auth_switch():
    usage_mode = config['usage_mode']
    if usage_mode == 'authenticated':
        AUTH_SWITCH.set_active(True)
    else:
        AUTH_SWITCH.set_active(False)


STT_COMBOBOX = builder.get_object("stt_combobox")
TTS_COMBOBOX = builder.get_object("tts_combobox")
AUTH_SWITCH = builder.get_object("auth_switch")
SNOWBOY_SWITCH = builder.get_object("snowboy_switch")
WAKE_BUTTON_SWITCH = builder.get_object("wake_button_switch")

init_stt_combobox()
init_tts_combobox()
init_auth_switch()

builder.connect_signals(Handler())

window.set_resizable(False)
window.show_all()

Gtk.main()
