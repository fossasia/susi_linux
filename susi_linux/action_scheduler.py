
import time
import sched
from threading import Thread
from rx.subject import Subject


class ActionScheduler(Thread):

    def __init__(self):
        super().__init__()
        self.subject = Subject()
        self.events = {}
        self.counter = -1
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def on_detected(self, reply):
        self.subject.on_next(reply)

    def add_event(self, delay, time, reply):
        if delay > 0:
            self.events[self.counter + 1] = self.scheduler.enter(delay, 0, self.on_detected, argument=(reply,))
        else:
            self.events[self.counter + 1] = self.scheduler.enterabs(time, 0, self.on_detected, argument=(reply,))
        self.counter += 1

    def run(self):
        while True:
            self.scheduler.run(blocking=True)
            time.sleep(1)
        return
