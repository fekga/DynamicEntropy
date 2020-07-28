# time_measurement.py

import time
from browser import window


class TimeMeasurment:
    def __init__(self):
        self.start_time = time.time()

    def getElapsedSeconds(self):
        return time.time() - self.start_time

    def printElapsedTime(self):
        hours, rem = divmod(self.getElapsedSeconds(), 3600)
        minutes, seconds = divmod(rem, 60)
        time_format = "{:0>2}h {:0>2}m {:02}s".format(int(hours), int(minutes), int(seconds))
        return f'{time_format}'

    # HACK for autosave
    def printRemainingTime(self, interval, element):
        elapsed = self.getElapsedSeconds()
        if elapsed > interval:
            self.start_time = time.time()
            event = window.MouseEvent.new("click")
            element.dispatchEvent(event)
        return f'{int(interval - self.getElapsedSeconds())}'