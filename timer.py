import time

class Task:
    def __init__(self, callback):
        """
        Construct an instance of a Task.
        """
        if not callable(callback):
            raise RuntimeError("Task to time must be a function.")
        self.callback = callback
        self.times = []

    def __str__(self):
        return "<Task: times %s>" % str(self.times)

def SimpleTimer(task):
    """
    Simple timer. Returns execution time

    args:
        task: function
    """
    if not callable(task):
        raise RuntimeError("Task to time must be a function.")
    start_time = time.time()
    task()
    end_time = time.time()
    return end_time - start_time

class Timer:
    """
    Construct an instance of a timer.

    This timer keeps track of a series of execution times for custom tasks,
    allowing batch test running and easy writing to file.
    """
    def __init__(self):
        self.tasks = {}

    def __str__(self):
        return "<Timer - %s tasks>" % len(self.tasks)

    def addTask(self, name, callback):
        """
        Add a task to the timer
        """
        if name in self.tasks:
            raise KeyError("That task already exists.")
        self.tasks[name] = Task(callback)

    def removeTask(self, name):
        """
        Remove a task from the timer
        """
        if name not in self.tasks:
            raise KeyError("That task doesn't exist.")
        del self.tasks[name]

    def _run(self, task):
        task.times.append(SimpleTimer(task.callback))

    def runOne(self, name):
        try:
            task = self.tasks[name]
        except KeyError:
            raise KeyError("This task doesn't exist.")
        self._run(task)

    def runAll(self):
        for task in self.tasks.values():
            self._run(task)

    @staticmethod
    def mean(iterable):
        return sum(iterable)/float(len(iterable))
        
    def getAvg(self, name):
        if name in self.tasks:
            return Timer.mean(self.tasks[name].times)
        else:
            raise KeyError("%s hasn't been successfully run!" % name)

    def flush(self, filename):
        with open(filename, 'w') as f:
            for key in self.tasks:
                f.write("%s\tAvg: %s\t%s\n" % (key, self.getAvg(key), str(self.tasks[key].times)))
