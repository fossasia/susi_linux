import os
import json_config
import gi
import logging

gi.require_version('Gtk', '3.0')  # nopep8

from pathlib import Path
from gi.repository import Gtk
from .login_window import LoginWindow

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')


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


class ConfigurationWindow:
    def __init__(self) -> None:
        super().__init__()
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(
            TOP_DIR, "glade_files/configure.glade"))

        self.window = builder.get_object("configuration_window")
        self.stt_combobox = builder.get_object("stt_combobox")
        self.tts_combobox = builder.get_object("tts_combobox")
        self.auth_switch = builder.get_object("auth_switch")
        self.snowboy_switch = builder.get_object("snowboy_switch")
        self.wake_button_switch = builder.get_object("wake_button_switch")

        self.init_auth_switch()
        self.init_tts_combobox()
        self.init_stt_combobox()
        self.init_hotword_switch()
        self.init_wake_button_switch()

        builder.connect_signals(ConfigurationWindow.Handler(self))
        self.window.set_resizable(False)

    def show_window(self):
        self.window.show_all()
        Gtk.main()

    def exit_window(self):
        self.window.destroy()
        Gtk.main_quit()

    def init_tts_combobox(self):
        default_tts = config['default_tts']
        if default_tts == 'google':
            self.tts_combobox.set_active(0)
        elif default_tts == 'flite':
            self.tts_combobox.set_active(1)
        elif default_tts == 'watson':
            self.tts_combobox.set_active(2)
        else:
            self.tts_combobox.set_active(0)
            config['default_tts'] = 'google'

    def init_stt_combobox(self):
        default_stt = config['default_stt']
        if default_stt == 'google':
            self.stt_combobox.set_active(0)
        elif default_stt == 'watson':
            self.stt_combobox.set_active(1)
        elif default_stt == 'bing':
            self.stt_combobox.set_active(2)
        else:
            self.tts_combobox.set_active(0)
            config['default_tts'] = 'google'

    def init_auth_switch(self):
        usage_mode = config['usage_mode']
        if usage_mode == 'authenticated':
            self.auth_switch.set_active(True)
        else:
            self.auth_switch.set_active(False)

    def init_hotword_switch(self):
        try:
            parent_dir = os.path.dirname(TOP_DIR)
            snowboyDetectFile = Path(os.path.join(
                parent_dir, "hotword_engine/snowboy/_snowboydetect.so"))
            print(snowboyDetectFile)
            if not snowboyDetectFile.exists():
                self.snowboy_switch.set_sensitive(False)
                config['hotword_engine'] = 'PocketSphinx'

        except Exception as e:
            logging.error(e)
            config['hotword_engine'] = 'PocketSphinx'

        if config['hotword_engine'] == 'Snowboy':
            self.snowboy_switch.set_active(True)
        else:
            self.snowboy_switch.set_active(False)

    def init_wake_button_switch(self):
        try:
            import RPi.GPIO
            if config['WakeButton'] == 'enabled':
                self.wake_button_switch.set_active(True)
            else:
                self.wake_button_switch.set_active(False)
        except ImportError:
            self.wake_button_switch.set_sensitive(False)

    class Handler:
        def __init__(self, config_window):
            self.config_window = config_window

        def on_delete_window(self, *args):
            print('Exiting')
            self.config_window.exit_window()

        def on_stt_combobox_changed(self, combo: Gtk.ComboBox):
            selection = combo.get_active()

            if selection == 0:
                config['default_stt'] = 'google'

            elif selection == 1:
                credential_dialog = WatsonCredentialsDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    username = credential_dialog.username_field.get_text()
                    password = credential_dialog.password_field.get_text()
                    config['default_stt'] = 'watson'
                    config['watson_stt_config']['username'] = username
                    config['watson_stt_config']['password'] = password
                else:
                    self.config_window.init_stt_combobox()

                credential_dialog.destroy()

            elif selection == 2:
                credential_dialog = BingCredentialDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    api_key = credential_dialog.api_key_field.get_text()
                    config['default_stt'] = 'bing'
                    config['bing_speech_api_key']['username'] = api_key
                else:
                    self.config_window.init_stt_combobox()

                credential_dialog.destroy()

        def on_tts_combobox_changed(self, combo):
            selection = combo.get_active()

            if selection == 0:
                config['default_tts'] = 'google'

            elif selection == 1:
                config['default_tts'] = 'flite'

            elif selection == 2:
                credential_dialog = WatsonCredentialsDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    username = credential_dialog.username_field.get_text()
                    password = credential_dialog.password_field.get_text()
                    config['default_tts'] = 'watson'
                    config['watson_tts_config']['username'] = username
                    config['watson_tts_config']['password'] = password
                    config['watson_tts_config']['voice'] = 'en-US_AllisonVoice'
                else:
                    self.config_window.init_tts_combobox()
                credential_dialog.destroy()

        def on_auth_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                login_window = LoginWindow()
                login_window.show_window()
                if config['usage_mode'] == 'authenticated':
                    switch.set_active(True)
                else:
                    switch.set_active(False)

        def on_snowboy_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                config['hotword_engine'] = 'Snowboy'
            else:
                config['hotword_engine'] = 'PocketSphinx'

        def on_wake_button_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                config['wake_button'] = 'enabled'
            else:
                config['wake_button'] = 'disabled'
