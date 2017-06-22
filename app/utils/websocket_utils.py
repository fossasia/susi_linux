import threading

from websocket_server import WebsocketServer


class WebsocketThread(threading.Thread):
    def __init__(self, port, fn_new_client, fn_client_left, fn_message_received):
        threading.Thread.__init__(self)
        server = WebsocketServer(port)
        server.set_fn_new_client(fn_new_client)
        server.set_fn_client_left(fn_client_left)
        server.set_fn_message_received(fn_message_received)
        self.server = server

    def run(self):
        self.server.run_forever()

    def send_to_all(self, message):
        self.server.send_message_to_all(message)