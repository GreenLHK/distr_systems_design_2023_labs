import requests
import time

from random_ip_port import *

import consul

def send_posts(num):
    for i in range(1,num+1):
        addr, port = random_addr_port(c,"facade_service")
        req_p = requests.post("http://"+addr+":"+str(port)+"/facade_service",json={"message": "msg"+str(i)})
        print('Send POST request to:','http//'+addr+':'+str(port))
        print(req_p.json())

def send_gets(num):
    for i in range(1,num+1):
        addr, port = random_addr_port(c, "facade_service")
        print('Send GET request to:', 'http//' + addr + ':' + str(port))
        req_g = requests.get("http://"+addr+":"+str(port)+"/facade_service")
        print(req_g.json())


c = consul.Consul()
send_posts(10)

send_gets(1)
time.sleep(20)
send_gets(2)


def put_key_value_in_consul_kv():
    c = consul.Consul()
    c.kv.put('hazelcast_path', r'D:\Навчання магістратура\2 семестр\Проект розпод систем\lab_microservices\hazelcast-4.2.7\bin\start.bat'.encode())
    c.kv.put('hazelcast_queue','queue')
    c.kv.put('hazelcast_map','lab-3-distributed-map')

#put_key_value_in_consul_kv()

'''
c = consul.Consul()

index, data = c.kv.get('hazelcast_path')
print(data['Value'].decode())
hazel_path = data['Value'].decode()
print(r''+hazel_path)

index, data = c.kv.get('hazelcast_queue')
print(data['Value'].decode())

index, data = c.kv.get('hazelcast_map')
print(data['Value'].decode())

'''

'''
index, services = c.health.service('facade_service', passing=True)
    #rand1 = dict()

for service_info in services:
    service = service_info['Service']
    print(service)
    #rand1[service['Address']] = service['Port']

index, services = c.health.service('logging_service', passing=True)
    #rand1 = dict()

for service_info in services:
    service = service_info['Service']
    print(service)
    #rand1[service['Address']] = service['Port']

index, services = c.health.service('messages_service', passing=True)
    #rand1 = dict()

for service_info in services:
    service = service_info['Service']
    print(service)
    #rand1[service['Address']] = service['Port']

'''