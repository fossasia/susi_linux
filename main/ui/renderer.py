from abc import ABC, abstractclassmethod
from rx.subjects import Subject
from .. import SusiStateMachine


class Renderer(ABC):
    def __init__(self):
        super().__init__()
        self.subject = Subject()
        self.susi_state_machine = SusiStateMachine(self)
        self.susi_state_machine.start()

    @abstractclassmethod
    def receive_message(self, message_type, payload=None):
        pass

    def on_mic_pressed(self):
        self.subject.on_next('mic_button_pressed')
