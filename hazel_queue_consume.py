import hazelcast
import threading
import time

client = hazelcast.HazelcastClient()

queue = client.get_queue("queue")


def consume(thr_id):
    consumed_count = 0
    while True:
        head = queue.take().result()
        print("Consuming {}, thread-{}".format(head,thr_id))
        consumed_count += 1
        if head == -1:
            print("Thread-{} finished consuming, consumed:{}".format(thr_id,consumed_count))
            break
        time.sleep(3)


consumer_thread = threading.Thread(target=consume,args=(1, ))

consumer_thread.start()
#time.sleep(1)
consumer_thread2 = threading.Thread(target=consume,args=(2, ))
consumer_thread2.start()
consumer_thread.join()
consumer_thread2.join()
client.shutdown()