import bluetooth
import json

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

print(f"Listening on port {port}...")
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

while True:
    data = client_sock.recv(1024)
    if not data:
        break
    data = data.decode('utf-8')
    print(f"Received: {data}")
    json_data = json.loads(data)
    print(f"Parsed JSON data: {json_data}")
    # Process the JSON data here
    json_data["response"] = "OK"
    response = json.dumps(json_data)
    client_sock.send(response.encode("utf-8"))

client_sock.close()
server_sock.close()