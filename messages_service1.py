from flask import Flask

app = Flask(__name__)

@app.route("/messages_service")
def get():
    return {"messager":"Message service temporary don't send messages"}

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=7069)

