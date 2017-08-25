import gi
import os
import json_config
import re
import requests
gi.require_version('Gtk', '3.0')  # nopep8

from gi.repository import Gtk
from gi.repository.Gdk import Color

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')


def is_valid(email, password):
    """ Method to Validate SUSI Login Details
    :param email: SUSI Sign-in email
    :param password: SUSI Sign-in password
    :return: boolean to indicate if details are valid
    """
    params = {
        'login': email,
        'password': password
    }
    sign_in_url = 'http://api.susi.ai/aaa/login.json?type=access-token'
    api_response = requests.get(sign_in_url, params)
    # except OSError:
    #     raise ConnectionError

    if api_response.status_code == 200:
        return True
    else:
        return False


class LoginWindow():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(
            TOP_DIR, "glade_files/signin.glade"))

        self.window = builder.get_object("login_window")
        self.email_field = builder.get_object("email_field")
        self.password_field = builder.get_object("password_field")
        self.spinner = builder.get_object("signin_spinner")
        self.sign_in_button = builder.get_object("signin_button")
        self.sign_in_button.set_sensitive(False)

        builder.connect_signals(LoginWindow.Handler(self))
        self.window.set_resizable(False)

    def show_window(self):
        self.window.show_all()
        Gtk.main()

    def exit_window(self):
        self.window.destroy()
        Gtk.main_quit()

    def show_successful_login_dialog(self):
        dialog = Gtk.MessageDialog(self.window, 0,
                                   Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                   "Login Successful")
        dialog.format_secondary_text(
            "Saving Login Details in configuration file.")
        dialog.run()
        dialog.destroy()
        self.exit_window()

    def show_failed_login_dialog(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL,
                                   "Incorrect Login Details")
        dialog.format_secondary_text("Please check your login details again.")
        dialog.run()
        dialog.destroy()

    def show_connection_error_dialog(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, "Internet connectivity problem")
        dialog.format_secondary_text(
            "There is some problem connecting to internet. Please make sure internet is working.")
        dialog.run()
        dialog.destroy()

    class Handler:
        def __init__(self, login_window):
            self.login_window = login_window

        def onDeleteWindow(self, *args):
            print('Exiting')
            self.login_window.exit_window()

        def signInButtonClicked(self, *args):
            COLOR_INVALID = Color(50000, 10000, 10000)
            email = self.login_window.email_field.get_text()
            password = self.login_window.password_field.get_text()

            result = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

            if result is None:
                print("None")
                self.login_window.email_field.modify_fg(
                    Gtk.StateFlags.NORMAL, COLOR_INVALID)
                return
            else:
                self.login_window.email_field.modify_fg(
                    Gtk.StateFlags.NORMAL, None)

            self.login_window.spinner.start()
            try:
                result = is_valid(email, password)
                if result:
                    self.login_window.spinner.stop()
                    self.login_window.show_successful_login_dialog()
                    config['usage_mode'] = 'authenticated'
                    config['login_credentials']['email'] = email
                    config['login_credentials']['password'] = password
                else:
                    self.login_window.spinner.stop()
                    self.login_window.show_failed_login_dialog()
                    config['usage_mode'] = 'anonymous'

            except ConnectionError:
                self.login_window.spinner.stop()
                self.login_window.show_connection_error_dialog()

            finally:
                self.login_window.spinner.stop()

        def input_changed(self, *args):
            email = self.login_window.email_field.get_text()
            password = self.login_window.password_field.get_text()

            result = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

            if result is not None and password is not '':
                self.login_window.sign_in_button.set_sensitive(True)
            else:
                self.login_window.sign_in_button.set_sensitive(False)
