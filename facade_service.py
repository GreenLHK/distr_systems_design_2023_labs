from flask import Flask
from flask import request
from flask import Response
from random import *
import uuid
import requests
import hazelcast
from flask import jsonify

#from flask_restful import Api, Resource
app = Flask(__name__)

def random_logger_port():
    return randint(1,3) + 7070

def random_messages_port():
    return 7070 - randint(1,2)

def send_post_random_logger(msg,msg_uuid):
    port = random_logger_port()
    req1 = requests.post("http://127.0.0.1:"+str(port)+"/logging_service", json={"msg": msg['message'], "msg_uuid": msg_uuid})
    return req1

def send_get_random_logger():
    port = random_logger_port()
    req1 = requests.get("http://127.0.0.1:"+str(port)+"/logging_service")
    return req1

def send_get_random_messages():
    port = random_messages_port()
    req1 = requests.get("http://127.0.0.1:"+str(port)+"/messages_service")
    return req1

def send_in_queue(msg):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    queue.put(msg)
    #client.shutdown()

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

app.run(debug=True, host="127.0.0.1", port=7070)
