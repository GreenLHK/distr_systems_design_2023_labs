from random import *

def random_service_port():
    return randint(1,10000) + 5000

def random_service_ip():
    ip = '127.0.'
    num1 = randint(0,255)
    num2 = randint(0,255)
    ip = ip + str(num1) + '.' + str(num2)
    return ip

def random_addr_port(c,service_name):
    #choose random service and return address and port
    index, services = c.health.service(service_name, passing=True)
    rand1 = dict()

    for service_info in services:
        service = service_info['Service']
        rand1[service['Address']] = service['Port']
    #print(rand1)
    if rand1 != {}:
        addr, prt = choice(list(rand1.items()))
    else:
        print("No services")
        addr, prt = None,None
    #print(addr, prt)
    return addr, prt

if __name__ == '__main__':
    print("contains functions for generating random ip address and port")
    print(random_service_ip()+':'+str(random_service_port()))