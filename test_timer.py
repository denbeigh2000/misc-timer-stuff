from timer import Timer
from time import sleep

timer = Timer()
def s1():
    sleep(1)

def s2():
    sleep(2)

def s3():
    sleep(3)

timer.addTask("sleep 1", s1)
timer.addTask("sleep 2", s2)
timer.addTask("sleep 3", s3)

timer.runAll()
timer.flush("test_timer.txt")
