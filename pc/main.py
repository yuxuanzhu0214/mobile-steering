import json
import socket
import vgamepad as vg
import time
from mapping import *
from helper import read_outauge
from update_buttons import update_gamepad

gamepad = vg.VX360Gamepad()

STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
PC1_BD_ADDR = "E0:94:67:F8:12:12"

bd_addr = STEERING_WHEEL2_BD_ADDR

port = 1
sock=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((bd_addr, port))
print(f"Connected to {bd_addr}...")


sock_outgauge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_outgauge.bind(('127.0.0.1', 4444))
print("Binding with game successful")


while True:
    button_inputs_json = sock.recv(1024).decode("utf-8")
    button_inputs = json.loads(button_inputs_json)
    print(f"Received response: {button_inputs}")

    gamepad = update_gamepad(button_inputs, gamepad)
    gamepad.update()


    # reading data from beamng.drive
    data = sock_outgauge.recv(1024)
    response = read_outauge(data)
    json_data = json.dumps(response)
    sock.send(json_data.encode("utf-8"))
    

sock.close()