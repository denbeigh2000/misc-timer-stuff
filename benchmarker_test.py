from benchmarker import Benchmarker
from time import sleep

bench = Benchmarker()

def s1():
    sleep(1)

def s2():
    sleep(2)

def s3():
    sleep(3)

bench.addTask("sleep 1", s1)
bench.addTask("sleep 2", s2)
bench.addTask("sleep 3", s3)

bench.run()
bench.displayTimes()
