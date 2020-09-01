from threading import Thread, Condition
import time

class TrackingThread (Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self._delay = delay
        self._interrupt = False
        self.cv = Condition()

    def stop(self):
        self._interrupt = True
        self.cv.acquire()
        self.cv.notify()
        self.cv.release()
        print("stop!!!")

    def run(self):
        self.cv.acquire()
        while not self._interrupt:
            print("llalala")
            self.cv.wait(self._delay)
        print("qqqqqq")
