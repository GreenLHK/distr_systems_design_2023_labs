from flask import Flask
from sys import argv
import hazelcast
import threading

app = Flask(__name__)

global msg_store
msg_store= list()

def get_msg_queue():
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    while True:
        head = queue.take().result()
        print("Consuming {}".format(head))
        msg_store.append(head["message"])



@app.route("/messages_service",methods=['GET'])
def get():

    return {"messager":msg_store}

if __name__ == '__main__':
    scr_name, port_num = argv
    print("Running messages_service on port",port_num)
    consumer_thread = threading.Thread(target=get_msg_queue)
    consumer_thread.daemon = True
    consumer_thread.start()
    app.run(debug=False, host="127.0.0.1", port=port_num)