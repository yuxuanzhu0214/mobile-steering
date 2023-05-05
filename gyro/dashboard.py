import json
import socket
import time
import requests

STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
STEERING_WHEEL1_BD_ADDR = "DC:A6:32:66:D8:A4"

PC1_BD_ADDR = "E0:94:67:F8:12:12"
LOCAL_BACKEND_URL = "http://127.0.0.1:3000/car"

bd_addr = STEERING_WHEEL1_BD_ADDR
server_sock=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

port = 2
server_sock.bind((bd_addr,port))
server_sock.listen(1)

print(f"Listening on port {port}...")
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

FPS = 20
sleep_time = 1/FPS
while True:
    data = client_sock.recv(1024)
    if not data:
        print("Invalid data, connection stopped...")
        break
    client_sock.send(b'A')
    resonse = data.decode('utf-8')
    data = json.loads(data)
    car_data = {}
    car_data["speed"] = data[0]
    car_data["rpm"] = data[1]
    car_data["gear"] = data[2]
    # post car info updates to backend
    requests.post(LOCAL_BACKEND_URL, json = car_data)
    print(f"Parsed JSON data: {car_data}")
    time.sleep(sleep_time)
client_sock.close()
server_sock.close()