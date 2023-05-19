from flask import Flask
from flask import request
from flask import Response
from random import *
import uuid
import requests

#from flask_restful import Api, Resource

def random_logger_port():
    return randint(1,3) + 7070

def send_post_random_logger(msg,msg_uuid):
    port = random_logger_port()
    req1 = requests.post("http://127.0.0.1:"+str(port)+"/logging_service", json={"msg": msg['message'], "msg_uuid": msg_uuid})
    return req1

def send_get_random_logger():
    port = random_logger_port()
    req1 = requests.get("http://127.0.0.1:"+str(port)+"/logging_service")
    return req1

app = Flask(__name__)

@app.route("/facade_service",methods=['GET'])
def get():
    req1 = None
    try:
        req1 = send_get_random_logger()
    except:
        print("Error")
    req2 = requests.get("http://127.0.0.1:7069/messages_service")
    resp1 = ''
    resp2 = ''
    try:
        for a in req1.json().values():
            resp1 = a
    except:
        resp1 = "error logging_service"
        print(resp1)

    try:
        for a in req2.json().values():
            resp2 = a
    except:
        resp2 = "error message_service"
        print(resp2)
    return {resp2:resp1}

@app.route("/facade_service",methods=['POST'])
def post():
    msg_uuid = str(uuid.uuid4())
    msg = request.get_json()
    print(msg)

    #req1 = requests.post("http://127.0.0.1:7071/logging_service",json={"msg":msg["msg"],"msg_uuid":msg_uuid})
    req1 = send_post_random_logger(msg,msg_uuid)

    return Response(
        req1.text,
        status=req1.status_code,
        content_type=req1.headers['content-type'],
    )

app.run(debug=True, host="127.0.0.1", port=7070)
