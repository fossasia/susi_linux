import os
import logging
import gi
gi.require_version('Gtk', '3.0')  # nopep8
from pathlib import Path
from gi.repository import Gtk
from .login_window import LoginWindow
from susi_config import SusiConfig

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
susicfg = SusiConfig()


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
        default_tts = susicfg.get('tts')
        if default_tts == 'google':
            self.tts_combobox.set_active(0)
        elif default_tts == 'flite':
            self.tts_combobox.set_active(1)
        elif default_tts == 'watson':
            self.tts_combobox.set_active(2)
        else:
            self.tts_combobox.set_active(0)
            susicfg.set('tts', 'google')

    def init_stt_combobox(self):
        default_stt = susicfg.get('stt')
        if default_stt == 'google':
            self.stt_combobox.set_active(0)
        elif default_stt == 'watson':
            self.stt_combobox.set_active(1)
        elif default_stt == 'bing':
            self.stt_combobox.set_active(2)
        elif default_stt == 'deepspeech-local':
            self.stt_combobox.set_active(3)
        else:
            self.tts_combobox.set_active(0)
            susicfg.set('tts', 'google')

    def init_auth_switch(self):
        usage_mode = susicfg.get('susi.mode')
        if usage_mode == 'authenticated':
            self.auth_switch.set_active(True)
        else:
            self.auth_switch.set_active(False)

    def init_hotword_switch(self):
        try:
            import snowboy
        except ImportError:
            self.snowboy_switch.set_sensitive(False)
            susicfg.set('hotword.engine', 'PocketSphinx')
        if susicfg.get('hotword.engine') == 'Snowboy':
            self.snowboy_switch.set_active(True)
        else:
            self.snowboy_switch.set_active(False)

    def init_wake_button_switch(self):
        try:
            import RPi.GPIO
            if susicfg.get('wakebutton') == 'enabled':
                self.wake_button_switch.set_active(True)
            else:
                self.wake_button_switch.set_active(False)
        except ImportError:
            self.wake_button_switch.set_sensitive(False)
        except RuntimeError:
            self.wake_button_switch.set_sensitive(False)

    class Handler:
        def __init__(self, config_window):
            self.config_window = config_window

        def on_delete_window(self, *args):
            self.config_window.exit_window()

        def on_stt_combobox_changed(self, combo: Gtk.ComboBox):
            selection = combo.get_active()

            if selection == 0:
                susicfg.set('stt', 'google')

            elif selection == 1:
                credential_dialog = WatsonCredentialsDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    username = credential_dialog.username_field.get_text()
                    password = credential_dialog.password_field.get_text()
                    susicfg.set('stt', 'watson')
                    susicfg.set('watson.stt.user', username)
                    susicfg.set('watson.stt.pass', password)
                else:
                    self.config_window.init_stt_combobox()

                credential_dialog.destroy()

            elif selection == 2:
                credential_dialog = BingCredentialDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    api_key = credential_dialog.api_key_field.get_text()
                    susicfg.set('stt', 'bing')
                    susicfg.set('bing.api', api_key)
                else:
                    self.config_window.init_stt_combobox()

                credential_dialog.destroy()

        def on_tts_combobox_changed(self, combo):
            selection = combo.get_active()

            if selection == 0:
                susicfg.set('tts', 'google')

            elif selection == 1:
                susicfg.set('tts', 'flite')

            elif selection == 2:
                credential_dialog = WatsonCredentialsDialog(
                    self.config_window.window)
                response = credential_dialog.run()

                if response == Gtk.ResponseType.OK:
                    username = credential_dialog.username_field.get_text()
                    password = credential_dialog.password_field.get_text()
                    susicfg.set('tts', 'watson')
                    susicfg.set('watson.tts.user', username)
                    susicfg.set('watson.tts.pass', password)
                    susicfg.set('watson.tts.voice', 'en-US_AllisonVoice')
                else:
                    self.config_window.init_tts_combobox()
                credential_dialog.destroy()

        def on_auth_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                login_window = LoginWindow()
                login_window.show_window()
                if susicfg.get('susi.mode') == 'authenticated':
                    switch.set_active(True)
                else:
                    switch.set_active(False)

        def on_snowboy_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                susicfg.set('hotword.engine', 'Snowboy')
            else:
                susicfg.set('hotword.engine', 'PocketSphinx')

        def on_wake_button_switch_active_notify(self, switch, gparam):
            if switch.get_active():
                susicfg.set('wakebutton', 'enabled')
            else:
                susicfg.set('wakebutton', 'disabled')
