# time_measurement.py

import time

class TimeMeasurment:
    start_time = time.time()

    def getElapsedSeconds():
        return time.time() - TimeMeasurment.start_time

    def printElapsedTime():
        hours, rem = divmod(TimeMeasurment.getElapsedSeconds(), 3600)
        minutes, seconds = divmod(rem, 60)
        time_format = "{:0>2}h {:0>2}m {:02}s".format(int(hours), int(minutes), int(seconds))
        return f'{time_format}'
