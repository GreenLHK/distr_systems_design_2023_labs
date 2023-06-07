from flask import Flask
from flask import request
from flask import Response
from random import *
import uuid
import requests
import hazelcast
from flask import jsonify
from random_ip_port import *
from sys import argv

import consul

#from flask_restful import Api, Resource
app = Flask(__name__)

def send_post_random_logger(msg,msg_uuid):
    addr, port = random_addr_port(c,'logging_service')
    req1 = requests.post("http://"+addr+":"+str(port)+"/logging_service", json={"msg": msg['message'], "msg_uuid": msg_uuid})
    return req1

def send_get_random_logger():
    addr, port = random_addr_port(c,'logging_service')
    req1 = requests.get("http://"+addr+":"+str(port)+"/logging_service")
    return req1

def send_get_random_messages():
    addr, port = random_addr_port(c,'messages_service')
    req1 = requests.get("http://"+addr+":"+str(port)+"/messages_service")
    return req1

def send_in_queue(msg):
    queue = client.get_queue(hazel_queue)
    queue.put(msg)

def send_get_for_full_messages():
    req = None
    print("Get all messages from messages_services")
    try:
        req = send_get_random_messages()
    except:
        print("Error")
    #answ1 = req.json().values()
    try:
        for a in req.json().values():
            answ1 = a
    except:
        answ1 = "error message_service"
        print(answ1)
    print(answ1)
    answ2 = answ1
    while answ2 == answ1:
        print("Next try")
        try:
            req = send_get_random_messages()
        except:
            print("Error")
            answ2 = []
        try:
            for a in req.json().values():
                answ2 = a
        except:
            answ2 = "error message_service"
            print(answ1)
    return answ1 + answ2

@app.route("/facade_service",methods=['GET'])
def get():
    req1 = None
    try:
        req1 = send_get_random_logger()
    except:
        print("Error")

    #req2 = requests.get("http://127.0.0.1:7069/messages_service")
    resp1 = ''
    #resp2 = ''
    try:
        for a in req1.json().values():
            resp1 = a
    except:
        resp1 = "error logging_service"
        print(resp1)

    resp2 = send_get_for_full_messages()
    print(resp2)
    return {"logger":resp1,"messages":resp2}

@app.route("/facade_service",methods=['POST'])
def post():
    msg_uuid = str(uuid.uuid4())
    msg = request.get_json()
    print(msg)

    #req1 = requests.post("http://127.0.0.1:7071/logging_service",json={"msg":msg["msg"],"msg_uuid":msg_uuid})
    req1 = send_post_random_logger(msg,msg_uuid)
    send_in_queue(msg)
    return Response(
        req1.text,
        status=req1.status_code,
        content_type=req1.headers['content-type'],
    )
    #return jsonify(result={"status": 200})

if __name__ == '__main__':
    #scr_name, port_num = argv
    service_addr= random_service_ip()
    service_port = random_service_port()
    service_uuid = str(uuid.uuid4())

    print("Running facade_service")
    print("Service address:", service_addr)
    print("Service port:", service_port)

    #register service in Consul
    c = consul.Consul()
    a = c.agent.Service(c)
    a.register(name="facade_service",service_id=service_uuid,address=service_addr,port=service_port)
    print('registered',service_uuid)

    # get Hazelcast queue config from Consul KV
    index, data = c.kv.get('hazelcast_queue')
    hazel_queue = data['Value'].decode()

    client = hazelcast.HazelcastClient()
    app.run(debug=False, host=service_addr, port=service_port)
    #Stop Hazelcast client after Flask shutdown
    client.shutdown()
    a.deregister(service_id=service_uuid)
    print("deregistered",service_uuid)