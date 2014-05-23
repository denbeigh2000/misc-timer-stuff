import subprocess
import time
from datetime import datetime

#from timer import Timer

HOUR = 5  # Start after 5 AM
DAY = 24  # Start only on the 24th

class Timer:
    def __init__(self):
        self.times = {}

    def run(self, name, *args):
        start_time = time.time()
        code = subprocess.call(args)
        end_time = time.time()
        if code != 0:
             raise RuntimeError("Call %s failed." % name)

        time_taken = end_time - start_time
        if name in self.times:
            self.times[name].append(time_taken)
        else:
            self.times[name] = [time_taken]

    def avg(self, name):
        if name in self.times:
            return sum(self.times[name])/float(len(self.times[name]))
        else:
            raise KeyError("%s hasn't been successfully run!" % name)

    def flush(self, filename):
        with open(filename, 'w') as f:
            for key in self.times:
                f.write(
                    "%s\tAvg: %s\t%s\n" %
                        (key, self.avg(key), str(self.times[key]))
                )

class RunBy:
    def __init__(self, callback, start=True, sleeptime=30, day=None,
            month=None, year=None, hour=None, minute=None, second=None):
        assert any([day, month, year, hour, minute, second]), \
                "You need to specify at least one time parameter."

        self.times = {
            'second': second,
            'minute': minute,
            'hour': hour,
            'day': day,
            'month': month,
            'year': year
        }

        self.callback = callback
        self.sleeptime = sleeptime

    def earlyEnough(self):
        now = datetime.now()
        for key, value in self.times.iteritems():
            if self.times[key] is None:
                continue
            if getattr(now, key) < value:
                return False;
        return True

    def run(self):
        print "Waiting..."
        while True:
            now = datetime.now()
            if self.earlyEnough():
                print "The time has come!"
                self.callback()
                break
            else:
                time.sleep(self.sleeptime)

#RunBy(runUniWork, day=24, hour=5)
r = RunBy(runUniWork, day=23, minute=32, sleeptime=5)
r.run()

