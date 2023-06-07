from flask import Flask
from sys import argv
import hazelcast
import threading
import consul
from random_ip_port import *
import uuid

app = Flask(__name__)

global msg_store
msg_store= list()

def get_msg_queue():

    client = hazelcast.HazelcastClient()
    queue = client.get_queue(hazel_queue)
    while True:
        head = queue.take().result()
        print("Consuming {}".format(head))
        msg_store.append(head["message"])



@app.route("/messages_service",methods=['GET'])
def get():

    return {"messager":msg_store}

if __name__ == '__main__':
    # scr_name, port_num = argv
    service_addr = random_service_ip()
    service_port = random_service_port()
    service_uuid = str(uuid.uuid4())

    print("Running messages_service")
    print("Service address:", service_addr)
    print("Service port:", service_port)

    # register service in Consul
    c = consul.Consul()
    a = c.agent.Service(c)
    a.register(name="messages_service", service_id=service_uuid, address=service_addr, port=service_port)
    print('registered', service_uuid)
    # get Hazelcast queue config from Consul KV
    index, data = c.kv.get('hazelcast_queue')
    hazel_queue = data['Value'].decode()
    consumer_thread = threading.Thread(target=get_msg_queue)
    consumer_thread.daemon = True
    consumer_thread.start()
    app.run(debug=False, host=service_addr, port=service_port)
    a.deregister(service_id=service_uuid)
    print("deregistered", service_uuid)
