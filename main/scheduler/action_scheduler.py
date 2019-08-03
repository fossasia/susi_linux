from threading import Thread
from rx.subject import Subject
import time
import sched

class ActionScheduler(Thread):

    def __init__(self):
        super().__init__()
        self.subject = Subject()
        print('START:', time.time())
        self.scheduler = sched.scheduler(time.time, time.sleep)
        e1 = self.scheduler.enter(10, 1, self.on_detected)

#super().on_detected()

    def on_detected(self):
        self.subject.on_next("Hotword")

    def run(self):
        print("runner is called")
        self.scheduler.run()
        return
