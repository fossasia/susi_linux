import os
import gi
import json_config
import re
import requests

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
config = json_config.connect('config.json')

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.Gdk import Color


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


def show_successful_login_dialog():
    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Login Successful")
    dialog.format_secondary_text("Saving Login Details in configuration file.")
    dialog.run()
    dialog.destroy()
    Gtk.main_quit()


def show_failed_login_dialog():
    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL, "Incorrect Login Details")
    dialog.format_secondary_text("Please check your login details again.")
    dialog.run()
    dialog.destroy()


def show_connection_error_dialog():
    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL, "Internet connectivity problem")
    dialog.format_secondary_text("There is some problem connecting to internet. Please make sure internet is working.")
    dialog.run()
    dialog.destroy()


class Handler:
    def onDeleteWindow(self, *args):
        print('Exiting')
        Gtk.main_quit(*args)

    def signInButtonClicked(self, *args):
        COLOR_INVALID = Color(50000, 10000, 10000)
        email = email_field.get_text()
        password = password_field.get_text()

        result = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        if result is None:
            print("None")
            email_field.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
            return
        else:
            email_field.modify_fg(Gtk.StateFlags.NORMAL, None)

        spinner.start()
        try:
            result = is_valid(email, password)
            if result:
                spinner.stop()
                show_successful_login_dialog()
                config['usage_mode'] = 'authenticated'
                config['login_credentials']['email'] = email
                config['login_credentials']['password'] = password
            else:
                spinner.stop()
                show_failed_login_dialog()
                config['usage_mode'] = 'anonymous'

        except ConnectionError:
            spinner.stop()
            show_connection_error_dialog()

        finally:
            spinner.stop()

    def input_changed(self, *args):
        email = email_field.get_text()
        password = password_field.get_text()

        result = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        if result is not None and password is not '':
            button.set_sensitive(True)
        else:
            button.set_sensitive(False)


builder = Gtk.Builder()
builder.add_from_file(os.path.join(TOP_DIR, "glade_files/signin.glade"))

window = builder.get_object("login_window")

email_field = builder.get_object("email_field")
password_field = builder.get_object("password_field")
spinner = builder.get_object("signin_spinner")
button = builder.get_object("signin_button")
button.set_sensitive(False)

builder.connect_signals(Handler())

window.set_resizable(False)
window.show_all()

Gtk.main()
