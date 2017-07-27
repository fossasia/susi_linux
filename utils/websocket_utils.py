""" This module defines utilities for communicating with SUSI Webchat interface
with WebSockets.
"""
import threading

from websocket_server import WebsocketServer


class WebsocketThread(threading.Thread):
    """ This class creates a WebSocket Server in background thread
    to communicate with SUSI Webchat interface in SUSI Webchat Connect Mode.
    """
    def __init__(self, port, fn_new_client, fn_client_left, fn_message_received):
        threading.Thread.__init__(self)
        server = WebsocketServer(host='0.0.0.0',port=port)
        server.set_fn_new_client(fn_new_client)
        server.set_fn_client_left(fn_client_left)
        server.set_fn_message_received(fn_message_received)
        self.server = server

    def run(self):
        self.server.run_forever()

    def send_to_all(self, message):
        self.server.send_message_to_all(message)