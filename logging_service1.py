import sys

from flask import Flask
from flask import request
from flask import jsonify
import subprocess
from sys import argv
import hazelcast
import readchar
import time


app = Flask(__name__)
global hazel_node
global server
msg_store = dict()

def write_in_hz_map(msg_uuid,msg):
    hz = hazelcast.HazelcastClient()

    map = hz.get_map("lab-3-distributed-map").blocking()
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
    map = hz.get_map("lab-3-distributed-map").blocking()
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
    scr_name, port_num = argv
    print("Running logging_service on port",port_num)
    hazel_node = subprocess.Popen(r'D:\Навчання магістратура\2 семестр\Проект розпод систем\lab_microservices\hazelcast-4.2.7\bin\start.bat',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    time.sleep(10)
    app.run(debug=False, host="127.0.0.1", port=port_num)
    hazel_node.terminate()

