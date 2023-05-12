import hazelcast
import logging

if __name__ == "__main__":
    hz = hazelcast.HazelcastClient()
    logging.basicConfig(level=logging.INFO)
    # Get the Distributed Map from Cluster.
    map = hz.get_map("lab-2-distributed-map").blocking()
    for i in range(1000):
        map.put(i, "value")
    print(map.get(2))
    hz.shutdown()




