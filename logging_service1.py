from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

msg_store = dict()

@app.route("/logging_service",methods=['GET'])
def get():
    cont = []
    for a in msg_store.values():
        cont.append(a)
    return {"Messages": cont}
@app.route("/logging_service",methods=['POST'])
def post():
    msg = request.get_json()
    msg_text = msg["msg"]
    msg_uuid = msg["msg_uuid"]
    print(msg_uuid,msg_text)
    msg_store[msg_uuid] = msg_text
    return jsonify(result={"status": 200})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=7071)