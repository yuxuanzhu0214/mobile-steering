import json
import socket
from mapping import *
import time
import requests

STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
PC1_BD_ADDR = "E0:94:67:F8:12:12"
# LOCAL_BACKEND_URL = "http://127.0.0.1:3000/car"

bd_addr = STEERING_WHEEL2_BD_ADDR
server_sock=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

port = 1
server_sock.bind((bd_addr,port))
server_sock.listen(1)

print(f"Listening on port {port}...")
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

count = 0
while True:
    #modify button input here
    button_inputs = {
    # value of 0(not pressed) to 1(pressed)
    DPAD_UP: 0,
    DPAD_DOWN: 0,
    DPAD_LEFT: 0,
    DPAD_RIGHT: 0,
    START: 0,
    BACK: 0,
    LEFT_THUMB: 0,
    RIGHT_THUMB: 0,
    LEFT_SHOULDER: 0,
    RIGHT_SHOULDER: 0,
    GUIDE: 0,
    A: 0,
    B: 0,
    X: 0,
    Y: 0,
    # value between 0 to 255
    LEFT_TRIG: 0,
    RIGHT_TRIG: 0,
    # value between -32768 and 32767
    LEFT_JOY_X: 0,
    LEFT_JOY_Y: 0,
    RIGHT_JOY_X: 0,
    RIGHT_JOY_Y: 0
    }

    json_inputs = json.dumps(button_inputs)
    client_sock.send(json_inputs.encode("utf-8"))
    response = client_sock.recv(1024)
    if not response:
        print("Invalid response, connection dropped...")
    
    
    # data = client_sock.recv(1024)
    # if not data:
    #     print("Invalid data, connection stopped...")
    #     break
    
    # resonse = data.decode('utf-8')
    # data = json.loads(data)
    # car_data = []
    # car_data["speed"] = data[0]
    # car_data["rpm"] = data[1]
    # car_data["gear"] = data[2]
    # # post car info updates to backend
    # requests.post(LOCAL_BACKEND_URL, json = car_data)
    # print(f"Parsed JSON data: {car_data}")

client_sock.close()
server_sock.close()