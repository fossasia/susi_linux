import os
import signal
import logging

import gi
import json_config

from . import ConfigurationWindow

gi.require_version('Gtk', '3.0')  # nopep8

from async_promises import Promise
from .animators import ListeningAnimator, ThinkingAnimator
from .renderer import Renderer
from gi.repository import Gtk

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')
logger = logging.getLogger(__name__)


class SusiAppWindow(Renderer):
    def __init__(self):
        super().__init__()
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(TOP_DIR, "glade_files/susi_app.glade"))

        self.window = builder.get_object("app_window")
        self.user_text_label = builder.get_object("user_text_label")
        self.susi_text_label = builder.get_object("susi_text_label")
        self.root_box = builder.get_object("root_box")
        self.state_stack = builder.get_object("state_stack")
        self.mic_button = builder.get_object("mic_button")
        self.mic_box = builder.get_object("mic_box")
        self.listening_box = builder.get_object("listening_box")
        self.thinking_box = builder.get_object("thinking_box")
        self.error_label = builder.get_object("error_label")
        self.settings_button = builder.get_object("settings_button")

        listeningAnimator = ListeningAnimator(self.window)
        self.listening_box.add(listeningAnimator)
        self.listening_box.reorder_child(listeningAnimator, 1)
        self.listening_box.set_child_packing(listeningAnimator, False, False, 0, Gtk.PackType.END)

        thinkingAnimator = ThinkingAnimator(self.window)
        self.thinking_box.add(thinkingAnimator)
        self.thinking_box.reorder_child(thinkingAnimator, 1)
        self.thinking_box.set_child_packing(thinkingAnimator, False, False, 0, Gtk.PackType.END)

        builder.connect_signals(SusiAppWindow.Handler(self))
        self.window.set_default_size(300, 600)
        self.window.set_resizable(False)

    def show_window(self):
        self.window.show_all()
        Gtk.main()

    def exit_window(self):
        self.window.destroy()
        Gtk.main_quit()

    def receive_message(self, message_type, payload=None):
        if message_type == 'idle':
            self.state_stack.set_visible_child_name("mic_page")

        elif message_type == 'listening':
            self.state_stack.set_visible_child_name("listening_page")
            self.user_text_label.set_text("")
            self.susi_text_label.set_text("")

        elif message_type == 'recognizing':
            self.state_stack.set_visible_child_name("thinking_page")

        elif message_type == 'recognized':
            user_text = payload
            self.user_text_label.set_text(user_text)

        elif message_type == 'speaking':
            self.state_stack.set_visible_child_name("empty_page")
            susi_reply = payload['susi_reply']
            if 'answer' in susi_reply.keys():
                self.susi_text_label.set_text(susi_reply['answer'])

        elif message_type == 'error':
            self.state_stack.set_visible_child_name("error_page")
            error_type = payload
            if error_type is not None:
                if error_type == 'connection':
                    self.error_label.set_text("Problem in internet connectivity !!")
                elif error_type == 'recognition':
                    self.error_label.set_text("Couldn't recognize the speech.")
            else:
                self.error_label.set_text('Some error occurred,')

    class Handler:
        def __init__(self, app_window):
            self.app_window = app_window

        def on_delete(self, *args):
            self.app_window.exit_window()
            os.kill(os.getppid(), signal.SIGHUP)

        def on_mic_button_clicked(self, button):
            Promise(
                lambda resolve, reject: resolve(self.app_window.on_mic_pressed())
            )

        def on_settings_button_clicked(self, button):
            window = ConfigurationWindow()
            window.show_window()
