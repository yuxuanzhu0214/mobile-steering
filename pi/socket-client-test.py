import socket
import time
HOST = "172.26.86.55"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    text = input("Enter the text: ")
    start_time = time.time()
    s.sendall(text.encode())
    data = s.recv(1024)
    end_time = time.time()
    print(f"Data received: {data.decode()}")
    elapsed_time = (end_time - start_time) * 1000
    print(f"Round trip time: {elapsed_time:.2f} ms")
