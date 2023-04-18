import json
import socket
import fcntl
from mapping import *
from helper import read_outauge


STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
PC1_BD_ADDR = "E0:94:67:F8:12:12"

bd_addr = STEERING_WHEEL2_BD_ADDR

port = 2
sock=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((bd_addr, port))
print(f"Connected to {bd_addr} on port {port}...")


while True:
    f = open('data.txt', 'r')
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    data = [int(line.strip()) for line in f]
    f.close()
    
    json_data = json.dumps(data)
    # send data to rpi
    sock.send(json_data.encode("utf-8"))
    response = sock.recv(1024)
