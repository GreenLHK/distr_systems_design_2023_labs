import requests
import time

def send_posts(num):
    for i in range(1,num+1):
        req_p = requests.post("http://127.0.0.1:7070/facade_service",json={"message": "msg"+str(i)})
        print(req_p.json())

send_posts(10)

req_g = requests.get("http://127.0.0.1:7070/facade_service")
print(req_g.json())

time.sleep(60)
req_g = requests.get("http://127.0.0.1:7070/facade_service")
print(req_g.json())

req_g = requests.get("http://127.0.0.1:7070/facade_service")
print(req_g.json())

req_g = requests.get("http://127.0.0.1:7070/facade_service")
print(req_g.json())
