import socket
PORT = 65431
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
host = s.getsockname()[0]
print(f"Server ip address: ", host)

# server code
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, PORT))
s.listen()
print(f"Listening for devices to connect at {host}:{PORT}")
conn, addr = s.accept()
with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        conn.sendall(data)
