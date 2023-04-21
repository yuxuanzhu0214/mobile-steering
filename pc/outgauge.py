import socket
from helper import read_outauge


sock_outgauge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_outgauge.bind(('127.0.0.1', 4444))
print("Binding with game successful")


while True:
    # reading data from beamng.drive
    data = sock_outgauge.recv(1024)
    if not data:
        print("Disconnected from game...")
        break
    response = read_outauge(data)
    #writing the output to data.txt
    f = open('data.txt', 'w')
    for num in response:
        f.write(str(num) + '\n')
    f.close()
    
sock_outgauge.close()

