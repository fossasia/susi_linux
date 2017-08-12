"""Class to represent Idle State
"""
import os

from .base_state import State


class IdleState(State):
    """Idle State inherits from the base state. In this state, app is actively listening for Hotword Input or Push
    Button Input. It transitions to Recognizing State upon successful detection.
    """

    def __init__(self, components):
        super().__init__(components)
        self.isActive = False
        self.components.hotword_detector.start()
        self.components.hotword_detector.subject.subscribe(on_next=lambda x: self.__detected())
        if self.components.wake_button is not None:
            self.components.wake_button.subject.subscribe(on_next=lambda x: self.__detected())

    def on_enter(self, payload=None):
        """Method to be executed on entry to Idle State. Detection is set to active.
        :param payload: Nothing is expected
        :return: None
        """
        self.isActive = True

    def __detected(self):
        if self.isActive:
            os.system('play {0} &'.format(self.components.config['detection_bell_sound']))
            self.transition(state=self.allowedStateTransitions.get('recognizing'), payload=None)

    def on_exit(self):
        """Method to be executed on exit from Idle State. Detection of Hotword and Wake Button is paused.
        :return: None
        """
        self.isActive = False
