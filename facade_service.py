from flask import Flask
from flask import request
from flask import Response
import uuid

#from flask_restful import Api, Resource

import requests

app = Flask(__name__)

@app.route("/facade_service",methods=['GET'])
def get():
    req1 = requests.get("http://127.0.0.1:7071/logging_service")
    req2 = requests.get("http://127.0.0.1:7072/messages_service")
    resp1 = ''
    resp2 = ''
    for a in req1.json().values():
        resp1 = a
    for a in req2.json().values():
        resp2 = a
    return {resp2:resp1}

@app.route("/facade_service",methods=['POST'])
def post():
    msg_uuid = uuid.uuid4()
    msg_uuid = str(msg_uuid)
    msg = request.get_json()
    print(msg)

    req1 = requests.post("http://127.0.0.1:7071/logging_service",json={"msg":msg["msg"],"msg_uuid":msg_uuid})
    return Response(
        req1.text,
        status=req1.status_code,
        content_type=req1.headers['content-type'],
    )
app.run(debug=True, host="127.0.0.1", port=7070)
