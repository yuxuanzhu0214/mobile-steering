from __future__ import print_function
import json
import socket
from mapping import *
import time

from ADC import *
# from IMU import *
from IMU_improved import *
from Buttons import Button_Matrix, rows, cols


ADC_in_0, ADC_in_1 = init_ADC()
IMU, angles = init_IMU()
Buttons = Button_Matrix(rows, cols)

STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
STEERING_WHEEL1_BD_ADDR = "DC:A6:32:66:D8:A4"

PC1_BD_ADDR = "E0:94:67:F8:12:12"
bd_addr = STEERING_WHEEL1_BD_ADDR
server_sock=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

port = 1
server_sock.bind((bd_addr,port))
server_sock.listen(1)

print(f"Listening on port {port}...")
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

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


count = 0
while True:
    

    # Update buttons
    Buttons.scan_buttons()
    for i in range(6):
        button_inputs[i] = Buttons.button_map[i]
    for i in [6,7]:
        button_inputs[i+2] = Buttons.button_map[i]
    for i in [8,9,10,11]:
        button_inputs[i+3] = Buttons.button_map[i]
    # Update ADC
    pot_v_in_0 = ADC_get_input(ADC_in_0, debug=False)
    pot_v_in_1 = ADC_get_input(ADC_in_1, debug=False)
    gas_pedal = int(pot_v_in_0 / 4.0 * 255.0)
    if gas_pedal > 245:
        gas_pedal = 0
    elif gas_pedal < 10:
        gas_pedal = 1
    button_inputs[RIGHT_TRIG] = gas_pedal
    brake_pedal = int(pot_v_in_1 / 4.0 * 255.0)
    if brake_pedal > 245:
        brake_pedal = 0
    elif brake_pedal < 10:
        brake_pedal = 1
    button_inputs[LEFT_TRIG] = brake_pedal
    # Update IMU
    euler_angle = IMU_get_angle(IMU, angles, debug=False)
    roll = euler_angle[0]
    steering_angle = roll
    # steering_angle = 1 * ((roll) / 120.0 * 32000.0) // 1000 * 1000
    steering_angle = roll // 5 * (32000/(120/5)) // 1000 * 1000
    if roll < 0:
        steering_angle = -1 * (-roll // 5 * (32000/(120/5))) // 1000 * 1000
    button_inputs[LEFT_JOY_X] = steering_angle
    print(f"roll angle {roll}; normalized joystick input {steering_angle}")

    # change LEFT_JOY_X and A for testing purposes
    # button_inputs[A] = count % 2
    # button_inputs[LEFT_JOY_X] = count % 32767
    count += 1

    json_inputs = json.dumps(button_inputs)
    client_sock.send(json_inputs.encode("utf-8"))
    data = client_sock.recv(1024)
    if not data:
        print("Invalid data, connection stopped...")
        break
    resonse = data.decode('utf-8')
    json_response = json.loads(data)
    # print(f"Parsed JSON data: {json_response}")
    time.sleep(0.05)

client_sock.close()
server_sock.close()
