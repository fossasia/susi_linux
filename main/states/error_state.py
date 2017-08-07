"""Class to represent Error State
"""
import os

from .base_state import State


class ErrorState(State):
    """Error State inherits from the State class. If any error is encountered in any state, it should transition to
    error mentioning the error in the payload.
    """
    def on_enter(self, payload=None):
        """Method executed on entry to Error State. Relevant error message is spoken.
        :param payload: String mentioning the error encountered.
        :return: None
        """
        if payload == 'RecognitionError':
            os.system('play extras/recognition-error.wav')
        elif payload == 'ConnectionError':
            os.system('play extras/connect-error.wav')
        else:
            os.system('play extras/problem.wav')

        self.transition(self.allowedStateTransitions.get('idle'))

    def on_exit(self):
        """Method executed on exit from the Error State.
        :return: None
        """
        pass
