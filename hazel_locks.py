import copy
import hazelcast
from threading import Thread
import logging

value = 0
key = '1'
logging.basicConfig(level=logging.INFO)
hz = hazelcast.HazelcastClient()
# Get the Distributed Map from Cluster.
map = hz.get_map("lab-2-distributed-map").blocking()

class Counter_for_threads():
    def __init__(self):
        self._counter = 0
    def increment(self):
        self._counter += 1
    def value(self):
        return self._counter
def no_blocking(map):
    # increment the counter
    for _ in range(2000):
        counter = map.get(key)
        counter.increment()
        map.set(key,counter)

def blocking_negative(map):
    # increment the counter
    for k in range(2000):
        map.lock(key)
        try:
            counter = map.get(key)
            counter.increment()
            map.set(key,counter)
        finally:
            map.unlock(key)
def blocking_positive(map):
    # increment the counter
    for k in range(2000):
        while True:
            old_value = map.get(key)
            new_value = copy.copy(old_value)
            new_value.increment()
            if map.replace_if_same(key,old_value, new_value):
                break

def start_threads(function):
    map.set(key, Counter_for_threads())
    threads = [Thread(target=function , args=(map,)) for _ in range(3)]
    # start all threads
    print("Starting " + str(function.__name__))
    for thread in threads:
        thread.start()
    # wait for all threads to finish
    for thread in threads:
        thread.join()
    print("Finished! Result = " + str(map.get(key).value()))
    # Shutdown this Hazelcast Client
    hz.shutdown()

#start_threads(no_blocking)
#start_threads(blocking_negative)
start_threads(blocking_positive)