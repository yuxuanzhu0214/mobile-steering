import bluetooth
import json

STEERING_WHEEL2_BD_ADDR = "E4:5F:01:BF:51:A8"
PC1_BD_ADDR = "E0:94:67:F8:12:12"

bd_addr = STEERING_WHEEL2_BD_ADDR

port = 1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
print(f"Connected to {bd_addr}...")

while True:
    message = input("Enter a message to send to the server: ")
    data = {"message": message}
    if data["message"] == "quit":
        break
    json_data = json.dumps(data)
    sock.send(json_data.encode("utf-8"))
    response = sock.recv(1024).decode("utf-8")
    response_data = json.loads(response)
    print(f"Received response: {response_data['response']}")

sock.close()