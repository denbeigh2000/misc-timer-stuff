from timer import SimpleTimer as Timer

from collections import Iterable

DEFAULT_RUNCOUNT = 5

def avg(itr):
    return sum(itr)/float(len(itr))

class Task:
    def __init__(self, key, callback, humanName=None, runCount=None, args=None,
                 kwargs=None):
        """
        Construct an instance of a Task
        args:
            key: string
            callback: function
            humanName: optional string - nicer representation on visuals
            runCount: number of times test is run benchmarking
        """
        if not callable(callback):
            raise RuntimeError("Callback is not a function.")
        self.times = []
        self.args = args or []
        self.kwargs = kwargs or {}
        self.key = key
        self.callback = callback
        self.runCount = runCount or DEFAULT_RUNCOUNT
        self.humanName = humanName or key

    def run(self):
        self.callback(*self.args, **self.kwargs)

class Benchmarker:
    def __init__(self, runCount=None):
        """
        Construct a Benchmarker instance
        params:
            runCount: optional int: set default number of runs for tasks in
                this benchmark test
        """
        self._tasks = {}
        self.runCount = runCount

    def run(self):
        """
        Run a benchmark test
        """
        if not self._tasks:
            raise RuntimeError("You need to add some tasks first.")
        for task in self._tasks.values():
            for _ in xrange(task.runCount):
                task.times.append(Timer(task.run))

    def addTask(self, key, callback, humanName=None, runCount=None):
        """
        Add a task to the benchmarking
        args:
            key: string
            callback: function - task to time
            humanName: optional string - nicer representation on pictures (soon)
            runCount: optional int - number of times to run in a benchmark test - default %s
        """ % DEFAULT_RUNCOUNT
        if key in self._tasks:
            raise KeyError("That task already exists.")
        if not runCount:
            runCount = self.runCount
        self._tasks[key] = Task(key, callback, humanName, runCount)

    def removeTask(self, key):
        """
        Remove a task from the benchmarking
        """
        if key not in self._tasks:
            raise KeyError("That task doesn't exist.")
        del self._tasks[key]

    def displayTimes(self):
        """
        Print a string representation to stdout
        """
        for task in self._tasks.values():
            print "%s\t%s\t%s" % (task.humanName, avg(task.times), task.times)
