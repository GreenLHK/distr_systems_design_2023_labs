import copy
import hazelcast
import time

def no_blocking(map):
    print("Start with no blocking")
    counter = 0
    if map.get(key) == None:
        map.set(key, 0)
    # increment the counter
    for _ in range(2000):
        counter = map.get(key)
        counter += 1
        map.set(key,counter)
    time.sleep(3)
    print("Finished! Result = " + str(map.get(key)))

def blocking_negative(map):
    print("Start negative blocking")
    counter = 0
    if map.get(key) == None:
        map.set(key,0)
    # increment the counter
    for k in range(2000):
        map.lock(key)
        try:
            counter = map.get(key)
            counter += 1
            map.set(key,counter)
        finally:
            map.unlock(key)
    time.sleep(3)
    print("Finished! Result = " + str(map.get(key)))
def blocking_positive(map):
    print("Start positive blocking")
    if map.get(key) == None:
        map.set(key, 0)
    # increment the counter
    for k in range(2000):
        while True:
            old_value = map.get(key)
            new_value = copy.copy(old_value)
            new_value += 1
            if map.replace_if_same(key,old_value, new_value):
                break
    time.sleep(5)
    print("Finished! Result = " + str(map.get(key)))


if __name__ == '__main__':
    value = 0
    key = '1'
    #logging.basicConfig(level=logging.INFO)
    hz = hazelcast.HazelcastClient()
    # Get the Distributed Map from Cluster.
    #print(time.time())
    time.sleep(1)
    map = hz.get_map("lab-2-distributed-map-no_block").blocking()
    no_blocking(map)
    hz.shutdown()
    time.sleep(4)

    hz = hazelcast.HazelcastClient()
    map = hz.get_map("lab-2-distributed-map-negative_block").blocking()
    blocking_negative(map)
    hz.shutdown()
    time.sleep(4)

    hz = hazelcast.HazelcastClient()
    map = hz.get_map("lab-2-distributed-map-positive_block").blocking()
    blocking_positive(map)
    hz.shutdown()