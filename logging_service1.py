import sys

from flask import Flask
from flask import request
from flask import jsonify
import subprocess
from sys import argv
import hazelcast
import readchar
import time

import consul
from random_ip_port import *
import uuid

app = Flask(__name__)
global hazel_node
global server
msg_store = dict()

def write_in_hz_map(msg_uuid,msg):
    hz = hazelcast.HazelcastClient()

    map = hz.get_map(hazel_map).blocking()
    try:
        map.put(msg_uuid,msg)
        print("Write key:",msg_uuid,"message:", msg)
    except:
        print("Can't write in map")

@app.route("/logging_service",methods=['GET'])
def get():
    cont = []
    for a in msg_store.values():
        cont.append(a)
    hz = hazelcast.HazelcastClient()
    map = hz.get_map(hazel_map).blocking()
    msg_hz = map.values()
    print(msg_hz)
    return {"Messages": msg_hz}
@app.route("/logging_service",methods=['POST'])
def post():
    msg = request.get_json()
    msg_text = msg["msg"]
    msg_uuid = msg["msg_uuid"]
    print(msg_uuid,msg_text)
    write_in_hz_map(msg_uuid,msg_text)
    #msg_store[msg_uuid] = msg_text
    return jsonify(result={"status": 200})

if __name__ == '__main__':
    # scr_name, port_num = argv
    service_addr = random_service_ip()
    service_port = random_service_port()
    service_uuid = str(uuid.uuid4())

    print("Running logging_service")
    print("Service address:", service_addr)
    print("Service port:", service_port)

    # register service in Consul
    c = consul.Consul()
    a = c.agent.Service(c)
    a.register(name="logging_service", service_id=service_uuid, address=service_addr, port=service_port)
    print('registered', service_uuid)
    #get Hazelcast node config from Consul KV
    index, data = c.kv.get('hazelcast_path')
    hazel_path = data['Value'].decode()
    hazel_node = subprocess.Popen(r''+hazel_path,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    # get map configuration from Consul KV
    index, data = c.kv.get('hazelcast_map')
    hazel_map = data['Value'].decode()
    time.sleep(10)
    app.run(debug=False, host=service_addr, port=service_port)
    hazel_node.terminate()
    a.deregister(service_id=service_uuid)
    print("deregistered", service_uuid)

