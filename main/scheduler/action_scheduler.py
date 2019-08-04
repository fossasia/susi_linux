from threading import Thread
from rx.subject import Subject
import time
import sched

class ActionScheduler(Thread):

    def __init__(self):
        super().__init__()
        self.subject = Subject()
        print('START:', time.time())
        self.events={}
        self.counter=-1
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def on_detected(self):
        self.subject.on_next("Hotword")

    def add_event(self,time):
        self.events[self.counter+1] = self.scheduler.enter(time, 0, self.on_detected)
        self.counter+=1
        print(self.events)

    def run(self):
        while True:
            self.scheduler.run(blocking=True)
            time.sleep(1)
        return
