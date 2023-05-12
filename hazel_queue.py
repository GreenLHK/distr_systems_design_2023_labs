import hazelcast
import threading
import time

client = hazelcast.HazelcastClient()

queue = client.get_queue("queue")

def produce():
    for i in range(1,25):
        time.sleep(0.5)
        queue.put("value-" + str(i))
        #queue.offer("value-" + str(i))
        #print("sent value-"+ str(i))
    #two -1 signals, because we have two threads for reading
    queue.put(-1)
    queue.put(-1)
    print("Finished writing in queue")
    print("Waiting...")
    time.sleep(60)
    print("Program finished")
producer_thread = threading.Thread(target=produce)
producer_thread.start()

producer_thread.join()

#client.shutdown()