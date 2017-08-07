"""Definition of Abstract Class State to represent Base State
"""
from abc import ABC, abstractclassmethod
import logging


class State(ABC):
    """State is an abstract class to represent a state. It defines the abstract method for behavior of state and
    transition method to facilitate transition between states.
    """
    def __init__(self, components):
        self.components = components
        self.allowedStateTransitions = {}

    @abstractclassmethod
    def on_enter(self, payload=None):
        """This method is executed on entry to a state. Perform the action designated for the state in this method.
        :param payload: an object to transfer information to the state. Default: None
        :return: None
        """
        pass

    @abstractclassmethod
    def on_exit(self):
        """This method is executed on exit from a state. Free up required resources or perform other important actions
        in this method
        :return: None
        """
        pass

    def transition(self, state, payload=None):
        """Execute this method to transition from one state to other valid state. Transition is only performed if valid.
        :param state: The state to which transition is to be performed.
        :param payload: any object that is needed to be transferred to next state.
        :return: None
        """
        if not self.__can_transition(state):
            print(self.allowedStateTransitions)
            logging.warning("Invalid transition to State: {0}".format(state))
            return

        self.on_exit()
        state.on_enter(payload)

    def __can_transition(self, state):
        return state in self.allowedStateTransitions.values()
